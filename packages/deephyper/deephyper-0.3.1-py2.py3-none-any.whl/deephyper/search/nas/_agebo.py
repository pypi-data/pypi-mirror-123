import collections

import numpy as np
import skopt

from deephyper.core.parser import str2bool
from deephyper.search.nas._regevo import RegularizedEvolution


class AgEBO(RegularizedEvolution):
    """`Aging evolution with Bayesian Optimization <https://arxiv.org/abs/2010.16358>`_.

    This algorithm build on the `Regularized Evolution <https://arxiv.org/abs/1802.01548>`_. It cumulates Hyperparameter optimization with Bayesian optimisation and Neural architecture search with regularized evolution.

    Args:
        problem (NaProblem): Hyperparameter problem describin the search space to explore.
        evaluator (Evaluator): An ``Evaluator`` instance responsible of distributing the tasks.
        random_state (int, optional): Random seed. Defaults to None.
        log_dir (str, optional): Log directory where search's results are saved. Defaults to ".".
        verbose (int, optional): Indicate the verbosity level of the search. Defaults to 0.
        population_size (int, optional): the number of individuals to keep in the population. Defaults to 100.
        sample_size (int, optional): the number of individuals that should participate in each tournament. Defaults to 10.
        surrogate_model (str, optional): Surrogate model used by the Bayesian optimization. Can be a value in ["RF", "ET", "GBRT", "DUMMY"]. Defaults to "RF".
        n_jobs (int, optional): Number of parallel processes used to fit the surrogate model of the Bayesian optimization. A value of -1 will use all available cores. Defaults to 1.
        kappa (float, optional): Manage the exploration/exploitation tradeoff for the "LCB" acquisition function. Defaults to 1.96 corresponds to 95% of the confidence interval.
        xi (float, optional): Manage the exploration/exploitation tradeoff of "EI" and "PI" acquisition function. Defaults to 0.001.
        acq_func (str, optional): Acquisition function used by the Bayesian optimization. Can be a value in ["LCB", "EI", "PI", "gp_hedge"]. Defaults to "LCB".
        liar_strategy (str, optional): Definition of the constant value use for the Liar strategy. Can be a value in ["cl_min", "cl_mean", "cl_max"] . Defaults to "cl_min".
        mode (str, optional): Define if the search should be asynchronous or batch synchronous. Choice in ["sync", "async"]. Defaults to "async".
    """

    def __init__(
        self,
        problem,
        evaluator,
        random_state: int = None,
        log_dir: str = ".",
        verbose: int = 0,
        # RE
        population_size: int = 100,
        sample_size: int = 10,
        # BO
        surrogate_model: str = "RF",
        n_jobs: int = 1,
        kappa: float = 0.001,
        xi: float = 0.000001,
        acq_func: str = "LCB",
        liar_strategy: str = "cl_min",
        mode: str = "async",
        **kwargs,
    ):
        super().__init__(
            problem,
            evaluator,
            random_state,
            log_dir,
            verbose,
            population_size,
            sample_size,
        )

        assert mode in ["sync", "async"]
        self.mode = mode

        self.n_jobs = int(n_jobs)  # parallelism of BO surrogate model estimator

        # Initialize opitmizer of hyperparameter space
        self._n_initial_points = self._evaluator.num_workers
        self._liar_strategy = liar_strategy

        if len(self._problem._hp_space._space) == 0:
            raise ValueError("No hyperparameter space was defined for this problem.")

        self._hp_opt = None
        self._hp_opt_kwargs = dict(
            dimensions=self._problem._hp_space._space,
            base_estimator=self._get_surrogate_model(surrogate_model, n_jobs),
            acq_func=acq_func,
            acq_optimizer="sampling",
            acq_func_kwargs={"xi": float(xi), "kappa": float(kappa)},
            n_initial_points=self._n_initial_points,
            random_state=self._random_state,
        )

    def _setup_hp_optimizer(self):
        self._hp_opt = skopt.Optimizer(**self._hp_opt_kwargs)

    def _saved_keys(self, job):

        res = {"arch_seq": str(job.config["arch_seq"])}
        hp_names = self._problem._hp_space._space.get_hyperparameter_names()

        for hp_name in hp_names:
            if hp_name == "loss":
                res["loss"] = job.config["loss"]
            else:
                res[hp_name] = job.config["hyperparameters"][hp_name]

        return res

    def _search(self, max_evals, timeout):

        if self._hp_opt is None:
            self._setup_hp_optimizer()

        num_evals_done = 0
        population = collections.deque(maxlen=self._population_size)

        # Filling available nodes at start
        self._evaluator.submit(self._gen_random_batch(size=self._n_initial_points))

        # Main loop
        while max_evals < 0 or num_evals_done < max_evals:

            # Collecting finished evaluations
            if self.mode == "async":
                new_results = list(self._evaluator.gather("BATCH", size=1))
            else:
                new_results = list(self._evaluator.gather("ALL"))

            if len(new_results) > 0:
                population.extend(new_results)

                self._evaluator.dump_evals(
                    saved_keys=self._saved_keys, log_dir=self._log_dir
                )

                num_received = len(new_results)
                num_evals_done += num_received

                hp_results_X, hp_results_y = [], []

                # If the population is big enough evolve the population
                if len(population) == self._population_size:
                    children_batch = []

                    # For each new parent/result we create a child from it
                    for new_i in range(len(new_results)):
                        # select_sample
                        indexes = np.random.choice(
                            self._population_size, self._sample_size, replace=False
                        )
                        sample = [population[i] for i in indexes]

                        # select_parent
                        parent = self._select_parent(sample)

                        # copy_mutate_parent
                        child = self._copy_mutate_arch(parent)

                        # add child to batch
                        children_batch.append(child)

                        # collect infos for hp optimization
                        new_i_hp_values = self._problem.extract_hp_values(
                            config=new_results[new_i][0]
                        )
                        new_i_y = new_results[new_i][1]
                        hp_results_X.append(new_i_hp_values)
                        hp_results_y.append(-new_i_y)

                    hp_results_y = np.minimum(hp_results_y, 1e3).tolist()  #! TODO

                    self._hp_opt.tell(hp_results_X, hp_results_y)  #! fit: costly
                    new_hps = self._hp_opt.ask(
                        n_points=len(new_results), strategy=self._liar_strategy
                    )

                    new_configs = []
                    for hp_values, child_arch_seq in zip(new_hps, children_batch):
                        new_config = self._problem.gen_config(child_arch_seq, hp_values)
                        new_configs.append(new_config)

                    # submit_childs
                    if len(new_results) > 0:
                        self._evaluator.submit(new_configs)

                else:  # If the population is too small keep increasing it

                    # For each new parent/result we create a child from it
                    for new_i in range(len(new_results)):

                        new_i_hp_values = self._problem.extract_hp_values(
                            config=new_results[new_i][0]
                        )
                        new_i_y = new_results[new_i][1]
                        hp_results_X.append(new_i_hp_values)
                        hp_results_y.append(-new_i_y)

                    self._hp_opt.tell(hp_results_X, hp_results_y)  #! fit: costly
                    new_hps = self._hp_opt.ask(
                        n_points=len(new_results), strategy=self._liar_strategy
                    )

                    new_batch = self._gen_random_batch(size=len(new_results), hps=new_hps)

                    self._evaluator.submit(new_batch)

    def _gen_random_batch(self, size: int, hps: list = None) -> list:
        batch = []
        if hps is None:
            points = self._hp_opt.ask(n_points=size)
            for hp_values in points:
                arch_seq = self._random_search_space()
                config = self._problem.gen_config(arch_seq, hp_values)
                batch.append(config)
        else:  # passed hps are used
            assert size == len(hps)
            for hp_values in hps:
                arch_seq = self._random_search_space()
                config = self._problem.gen_config(arch_seq, hp_values)
                batch.append(config)
        return batch

    def _copy_mutate_arch(self, parent_arch: list) -> list:
        """
        # ! Time performance is critical because called sequentialy

        Args:
            parent_arch (list(int)): embedding of the parent's architecture.

        Returns:
            dict: embedding of the mutated architecture of the child.

        """
        i = np.random.choice(len(parent_arch))
        child_arch = parent_arch[:]

        range_upper_bound = self.space_list[i][1]
        elements = [j for j in range(range_upper_bound + 1) if j != child_arch[i]]

        # The mutation has to create a different search_space!
        sample = np.random.choice(elements, 1)[0]

        child_arch[i] = sample
        return child_arch

    def _get_surrogate_model(self, name: str, n_jobs: int = None):
        """Get a surrogate model from Scikit-Optimize.

        Args:
            name (str): name of the surrogate model.
            n_jobs (int): number of parallel processes to distribute the computation of the surrogate model.

        Raises:
            ValueError: when the name of the surrogate model is unknown.
        """
        accepted_names = ["RF", "ET", "GBRT", "GP", "DUMMY"]
        if not (name in accepted_names):
            raise ValueError(
                f"Unknown surrogate model {name}, please choose among {accepted_names}."
            )

        if name == "RF":
            surrogate = skopt.learning.RandomForestRegressor(n_jobs=n_jobs)
        elif name == "ET":
            surrogate = skopt.learning.ExtraTreesRegressor(n_jobs=n_jobs)
        elif name == "GBRT":
            surrogate = skopt.learning.GradientBoostingQuantileRegressor(n_jobs=n_jobs)
        else:  # for DUMMY and GP
            surrogate = name

        return surrogate
