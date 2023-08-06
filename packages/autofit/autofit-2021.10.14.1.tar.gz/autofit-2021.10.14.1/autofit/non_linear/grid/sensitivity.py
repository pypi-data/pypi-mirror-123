import logging
from copy import copy
from itertools import count
from typing import List, Generator, Callable, Type, Union, Tuple

from autofit.mapper.model import ModelInstance
from autofit.mapper.prior_model.abstract import AbstractPriorModel
from autofit.non_linear.abstract_search import NonLinearSearch
from autofit.non_linear.analysis import Analysis
from autofit.non_linear.grid.grid_search import make_lists
from autofit.non_linear.parallel import AbstractJob, Process, AbstractJobResult
from autofit.non_linear.result import Result


class JobResult(AbstractJobResult):
    def __init__(
            self,
            number: int,
            result: Result,
            perturbed_result: Result
    ):
        """
        The result of a single sensitivity comparison

        Parameters
        ----------
        result
        perturbed_result
        """
        super().__init__(number)
        self.result = result
        self.perturbed_result = perturbed_result

    @property
    def log_likelihood_difference(self):
        return self.perturbed_result.log_likelihood - self.result.log_likelihood


class Job(AbstractJob):
    _number = count()

    def __init__(
            self,
            analysis: Analysis,
            model: AbstractPriorModel,
            perturbation_model: AbstractPriorModel,
            search: NonLinearSearch
    ):
        """
        Job to run non-linear searches comparing how well a model and a model with a perturbation
        fit the image.

        Parameters
        ----------
        model
            A base model that fits the image without a perturbation
        perturbation_model
            A model of the perturbation which has been added to the underlying image
        analysis
            A class definition which can compares instances of a model to a perturbed image
        search
            A non-linear search
        """
        super().__init__()

        self.analysis = analysis
        self.model = model

        self.perturbation_model = perturbation_model

        self.search = search.copy_with_paths(
            search.paths.for_sub_analysis(
                "[base]",
            )
        )
        self.perturbed_search = search.copy_with_paths(
            search.paths.for_sub_analysis(
                "[perturbed]",
            )
        )

    def perform(self) -> JobResult:
        """
        - Create one model with a perturbation and another without
        - Fit each model against the perturbed image

        Returns
        -------
        An object comprising the results of the two fits
        """
        result = self.search.fit(
            model=self.model,
            analysis=self.analysis
        )

        perturbed_model = copy(self.model)
        perturbed_model.perturbation = self.perturbation_model

        perturbed_result = self.perturbed_search.fit(
            model=perturbed_model,
            analysis=self.analysis
        )
        return JobResult(
            number=self.number,
            result=result,
            perturbed_result=perturbed_result
        )


class SensitivityResult:

    def __init__(self, results: List[JobResult]):
        self.results = sorted(results)

    def __getitem__(self, item):
        return self.results[item]

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)


class Sensitivity:

    def __init__(
            self,
            base_model: AbstractPriorModel,
            perturbation_model: AbstractPriorModel,
            simulation_instance,
            simulate_function: Callable,
            analysis_class: Type[Analysis],
            search: NonLinearSearch,
            number_of_steps: Union[Tuple[int], int] = 4,
            number_of_cores: int = 2
    ):
        """
        Perform sensitivity mapping to evaluate whether a perturbation
        can be detected if it occurs in different parts of an image.

        For a range from 0 to 1 with step_size, for each dimension of the
        perturbation_model, a perturbation is created and used in conjunction
        with the instance to create an image.

        For each of these images, a fit is run with just the model and with both
        the model and perturbation_model to compare how much better the image
        can be fit if the perturbation is included.

        Parameters
        ----------
        simulation_instance
            An instance of a model to which perturbations are applied prior to
            images being generated
        base_model
            A model that fits the instance well
        search
            A NonLinear search class which is copied and used to evaluate fitness
        analysis_class
            A class which can compare an image to an instance and evaluate fitness
        perturbation_model
            A model which provides a perturbations to be applied to the instance
            before creating images
        simulate_function
            A function that can convert an instance into an image
        number_of_cores
            How many cores does this computer have? Minimum 2.
        """
        self.logger = logging.getLogger(
            f"Sensitivity ({search.name})"
        )

        self.logger.info("Creating")

        self.instance = simulation_instance
        self.model = base_model

        self.search = search
        self.analysis_class = analysis_class

        self.number_of_steps = number_of_steps
        self.perturbation_model = perturbation_model
        self.simulate_function = simulate_function
        self.number_of_cores = number_of_cores or 2

    @property
    def step_size(self):
        """
        Returns
        -------
        step_size: float
            The size of a step in any given dimension in hyper space.
        """
        if isinstance(self.number_of_steps, tuple):
            return tuple([1 / number_of_steps for number_of_steps in self.number_of_steps])
        return 1 / self.number_of_steps

    def run(self) -> SensitivityResult:
        """
        Run fits and comparisons for all perturbations, returning
        a list of results.
        """
        self.logger.info("Running")
        results = list()
        for result in Process.run_jobs(
                self._make_jobs(),
                number_of_cores=self.number_of_cores
        ):
            results.append(result)
        return SensitivityResult(results)

    @property
    def _lists(self) -> List[List[float]]:
        """
        A list of hypercube vectors, used to instantiate
        the perturbation_model and create the individual
        perturbations.
        """
        return make_lists(
            self.perturbation_model.prior_count,
            step_size=self.step_size
        )

    @property
    def _labels(self) -> Generator[str, None, None]:
        """
        One label for each perturbation, used to distinguish
        fits for each perturbation by placing them in separate
        directories.
        """
        for list_ in self._lists:
            strings = list()
            for value, prior_tuple in zip(
                    list_,
                    self.perturbation_model.prior_tuples
            ):
                path, prior = prior_tuple
                value = prior.value_for(
                    value
                )
                strings.append(
                    f"{path}_{value}"
                )
            yield "_".join(strings)

    @property
    def _perturbation_instances(self) -> Generator[
        ModelInstance, None, None
    ]:
        """
        A list of instances each of which defines a perturbation to
        be applied to the image.
        """
        for list_ in self._lists:
            yield self.perturbation_model.instance_from_unit_vector(
                list_
            )

    @property
    def _searches(self) -> Generator[
        NonLinearSearch, None, None
    ]:
        """
        A list of non-linear searches, each of which is applied to
        one perturbation.
        """
        for label in self._labels:
            yield self._search_instance(
                label
            )

    def _search_instance(
            self,
            name_path: str
    ) -> NonLinearSearch:
        """
        Create a search instance, distinguished by its name

        Parameters
        ----------
        name_path
            A path to distinguish this search from other searches

        Returns
        -------
        A non linear search, copied from the instance search
        """
        paths = self.search.paths
        search_instance = self.search.copy_with_paths(
            paths.for_sub_analysis(
                name_path,
            )
        )

        return search_instance

    def _make_jobs(self) -> Generator[Job, None, None]:
        """
        Create a list of jobs to be run on separate processes.

        Each job fits a perturbed image with the original model
        and a model which includes a perturbation.
        """
        for perturbation_instance, search in zip(
                self._perturbation_instances,
                self._searches
        ):
            instance = copy(self.instance)
            instance.perturbation = perturbation_instance
            dataset = self.simulate_function(
                instance
            )
            yield Job(
                analysis=self.analysis_class(
                    dataset
                ),
                model=self.model,
                perturbation_model=self.perturbation_model,
                search=search
            )
