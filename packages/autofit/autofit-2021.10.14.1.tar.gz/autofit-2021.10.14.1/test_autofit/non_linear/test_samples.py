import os

import pytest

import autofit as af
import autofit.non_linear.samples.nest
import autofit.non_linear.samples.pdf
from autofit.mock.mock import MockClassx2, MockClassx4
from autofit.non_linear.samples import Sample

import numpy as np

pytestmark = pytest.mark.filterwarnings("ignore::FutureWarning")


class MockSamples(autofit.non_linear.samples.pdf.PDFSamples):

    def __init__(
            self,
            model,
            sample_list=None,
            unconverged_sample_size=10,
            **kwargs,
    ):

        super().__init__(
            model=model,
            sample_list=sample_list,
            unconverged_sample_size=unconverged_sample_size,  **kwargs
        )

@pytest.fixture(name="samples")
def make_samples():
    model = af.ModelMapper(mock_class_1=MockClassx4)

    parameters = [
        [0.0, 1.0, 2.0, 3.0],
        [0.0, 1.0, 2.0, 3.0],
        [0.0, 1.0, 2.0, 3.0],
        [21.0, 22.0, 23.0, 24.0],
        [0.0, 1.0, 2.0, 3.0],
    ]

    return MockSamples(
        model=model,
        sample_list=Sample.from_lists(
            model=model,
            parameter_lists=parameters,
            log_likelihood_list=[1.0, 2.0, 3.0, 10.0, 5.0],
            log_prior_list=[0.0, 0.0, 0.0, 0.0, 0.0],
            weight_list=[1.0, 1.0, 1.0, 1.0, 1.0],
        )
    )


class TestSamplesTable:
    def test_headers(self, samples):
        assert samples._headers == [
            "mock_class_1_one",
            "mock_class_1_two",
            "mock_class_1_three",
            "mock_class_1_four",
            "log_likelihood",
            "log_prior",
            "log_posterior",
            "weight",
        ]

    def test_rows(self, samples):
        rows = list(samples._rows)
        assert rows == [
            [0.0, 1.0, 2.0, 3.0, 1.0, 0.0, 1.0, 1.0],
            [0.0, 1.0, 2.0, 3.0, 2.0, 0.0, 2.0, 1.0],
            [0.0, 1.0, 2.0, 3.0, 3.0, 0.0, 3.0, 1.0],
            [21.0, 22.0, 23.0, 24.0, 10.0, 0.0, 10.0, 1.0],
            [0.0, 1.0, 2.0, 3.0, 5.0, 0.0, 5.0, 1.0],
        ]

    def test__write_table(self, samples):
        filename = "samples.csv"
        samples.write_table(filename=filename)

        assert os.path.exists(filename)
        os.remove(filename)


class TestOptimizerSamples:
    def test__max_log_likelihood_vector_and_instance(self, samples):
        assert samples.max_log_likelihood_vector == [21.0, 22.0, 23.0, 24.0]

        instance = samples.max_log_likelihood_instance

        assert instance.mock_class_1.one == 21.0
        assert instance.mock_class_1.two == 22.0
        assert instance.mock_class_1.three == 23.0
        assert instance.mock_class_1.four == 24.0

    def test__log_prior_list_and_max_log_posterior_vector_and_instance(self):
        model = af.ModelMapper(mock_class_1=MockClassx4)

        parameters = [
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [21.0, 22.0, 23.0, 24.0],
        ]

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=[1.0, 2.0, 3.0, 0.0, 5.0],
                log_prior_list=[1.0, 2.0, 3.0, 10.0, 6.0],
                weight_list=[1.0, 1.0, 1.0, 1.0, 1.0],
            )
        )

        assert samples.log_posterior_list == [2.0, 4.0, 6.0, 10.0, 11.0]

        assert samples.max_log_posterior_vector == [21.0, 22.0, 23.0, 24.0]

        instance = samples.max_log_posterior_instance

        assert instance.mock_class_1.one == 21.0
        assert instance.mock_class_1.two == 22.0
        assert instance.mock_class_1.three == 23.0
        assert instance.mock_class_1.four == 24.0

    def test__gaussian_priors(self):
        parameters = [
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.1],
            [1.0, 2.0, 3.0, 4.1],
            [0.88, 1.88, 2.88, 3.88],
            [1.12, 2.12, 3.12, 4.32],
        ]

        model = af.ModelMapper(mock_class=MockClassx4)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=[10.0, 0.0, 0.0, 0.0, 0.0],
                log_prior_list=[0.0, 0.0, 0.0, 0.0, 0.0],
                weight_list=[1.0, 1.0, 1.0, 1.0, 1.0],

            ))

        gaussian_priors = samples.gaussian_priors_at_sigma(sigma=1.0)

        assert gaussian_priors[0][0] == 1.0
        assert gaussian_priors[1][0] == 2.0
        assert gaussian_priors[2][0] == 3.0
        assert gaussian_priors[3][0] == 4.0

        assert gaussian_priors[0][1] == pytest.approx(0.12, 1.0e-4)
        assert gaussian_priors[1][1] == pytest.approx(0.12, 1.0e-4)
        assert gaussian_priors[2][1] == pytest.approx(0.12, 1.0e-4)
        assert gaussian_priors[3][1] == pytest.approx(0.32, 1.0e-4)

    def test__instance_from_sample_index(self):
        model = af.ModelMapper(mock_class=MockClassx4)

        parameters = [
            [1.0, 2.0, 3.0, 4.0],
            [5.0, 6.0, 7.0, 8.0],
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.0],
            [1.1, 2.1, 3.1, 4.1],
        ]

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=[0.0, 0.0, 0.0, 0.0, 0.0],
                log_prior_list=[0.0, 0.0, 0.0, 0.0, 0.0],
                weight_list=[1.0, 1.0, 1.0, 1.0, 1.0],

            ))

        instance = samples.instance_from_sample_index(sample_index=0)

        assert instance.mock_class.one == 1.0
        assert instance.mock_class.two == 2.0
        assert instance.mock_class.three == 3.0
        assert instance.mock_class.four == 4.0

        instance = samples.instance_from_sample_index(sample_index=1)

        assert instance.mock_class.one == 5.0
        assert instance.mock_class.two == 6.0
        assert instance.mock_class.three == 7.0
        assert instance.mock_class.four == 8.0


class TestPDFSamples:
    def test__from_csv_table(self, samples):
        filename = "samples.csv"
        samples.write_table(filename=filename)

        samples = autofit.non_linear.samples.nest.NestSamples.from_table(filename=filename, model=samples.model)

        assert samples.parameter_lists == [
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [21.0, 22.0, 23.0, 24.0],
            [0.0, 1.0, 2.0, 3.0],
        ]
        assert samples.log_likelihood_list == [1.0, 2.0, 3.0, 10.0, 5.0]
        assert samples.log_prior_list == [0.0, 0.0, 0.0, 0.0, 0.0]
        assert samples.log_posterior_list == [1.0, 2.0, 3.0, 10.0, 5.0]
        assert samples.weight_list == [1.0, 1.0, 1.0, 1.0, 1.0]

    def test__converged__median_pdf_vector_and_instance(self):
        parameters = [
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [0.9, 1.9],
            [1.1, 2.1],
        ]

        log_likelihood_list = 10 * [0.1]
        weight_list = 10 * [0.1]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            )
        )

        assert samples.pdf_converged is True

        median_pdf_vector = samples.median_pdf_vector

        assert median_pdf_vector[0] == pytest.approx(1.0, 1.0e-4)
        assert median_pdf_vector[1] == pytest.approx(2.0, 1.0e-4)

        median_pdf_instance = samples.median_pdf_instance

        assert median_pdf_instance.mock_class.one == pytest.approx(1.0, 1e-1)
        assert median_pdf_instance.mock_class.two == pytest.approx(2.0, 1e-1)

    def test__unconverged__median_pdf_vector(self):
        parameters = [
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.1, 2.1],
            [0.9, 1.9],
        ]

        log_likelihood_list = 9 * [0.0] + [1.0]
        weight_list = 9 * [0.0] + [1.0]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.pdf_converged is False

        median_pdf_vector = samples.median_pdf_vector

        assert median_pdf_vector[0] == pytest.approx(0.9, 1.0e-4)
        assert median_pdf_vector[1] == pytest.approx(1.9, 1.0e-4)

    def test__converged__vector_and_instance_at_upper_and_lower_sigma(self):
        parameters = [
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.0, 0.5],
            [0.2, 0.3],
        ]

        log_likelihood_list = list(range(10))

        weight_list = 10 * [0.1]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.pdf_converged is True

        vector_at_sigma = samples.vector_at_sigma(sigma=3.0)

        assert vector_at_sigma[0] == pytest.approx((0.00121, 0.19878), 1e-1)
        assert vector_at_sigma[1] == pytest.approx((0.30121, 0.49878), 1e-1)

        vector_at_sigma = samples.vector_at_upper_sigma(sigma=3.0)

        assert vector_at_sigma[0] == pytest.approx(0.19757, 1e-1)
        assert vector_at_sigma[1] == pytest.approx(0.49757, 1e-1)

        vector_at_sigma = samples.vector_at_lower_sigma(sigma=3.0)

        assert vector_at_sigma[0] == pytest.approx(0.00121, 1e-1)
        assert vector_at_sigma[1] == pytest.approx(0.30121, 1e-1)

        vector_at_sigma = samples.vector_at_sigma(sigma=1.0)

        assert vector_at_sigma[0] == pytest.approx((0.1, 0.1), 1e-1)
        assert vector_at_sigma[1] == pytest.approx((0.4, 0.4), 1e-1)

        instance_at_sigma = samples.instance_at_sigma(sigma=1.0)

        assert instance_at_sigma.mock_class.one == pytest.approx((0.1, 0.1), 1e-1)
        assert instance_at_sigma.mock_class.two == pytest.approx((0.4, 0.4), 1e-1)

        instance_at_sigma = samples.instance_at_upper_sigma(sigma=3.0)

        assert instance_at_sigma.mock_class.one == pytest.approx(0.19757, 1e-1)
        assert instance_at_sigma.mock_class.two == pytest.approx(0.49757, 1e-1)

        instance_at_sigma = samples.instance_at_lower_sigma(sigma=3.0)

        assert instance_at_sigma.mock_class.one == pytest.approx(0.00121, 1e-1)
        assert instance_at_sigma.mock_class.two == pytest.approx(0.30121, 1e-1)

    def test__unconverged_vector_at_lower_and_upper_sigma(self):
        parameters = [
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.0, 2.0],
            [1.1, 2.1],
            [0.9, 1.9],
        ]

        log_likelihood_list = 9 * [0.0] + [1.0]
        weight_list = 9 * [0.0] + [1.0]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.pdf_converged is False

        vector_at_sigma = samples.vector_at_sigma(sigma=1.0)

        assert vector_at_sigma[0] == pytest.approx(((0.9, 1.1)), 1e-2)
        assert vector_at_sigma[1] == pytest.approx(((1.9, 2.1)), 1e-2)

        vector_at_sigma = samples.vector_at_sigma(sigma=3.0)

        assert vector_at_sigma[0] == pytest.approx(((0.9, 1.1)), 1e-2)
        assert vector_at_sigma[1] == pytest.approx(((1.9, 2.1)), 1e-2)

    def test__converged__errors_vector_and_instance_at_upper_and_lower_sigma(self):
        parameters = [
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.1, 0.4],
            [0.0, 0.5],
            [0.2, 0.3],
        ]

        log_likelihood_list = list(range(10))

        weight_list = 10 * [0.1]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.pdf_converged is True

        errors = samples.error_magnitude_vector_at_sigma(sigma=3.0)

        assert errors == pytest.approx([0.19514, 0.19514], 1e-1)

        errors = samples.error_vector_at_upper_sigma(sigma=3.0)

        assert errors == pytest.approx([0.09757, 0.09757], 1e-1)

        errors = samples.error_vector_at_lower_sigma(sigma=3.0)

        assert errors == pytest.approx([0.09757, 0.09757], 1e-1)

        errors = samples.error_vector_at_sigma(sigma=3.0)
        assert errors[0] == pytest.approx((0.09757, 0.09757), 1e-1)
        assert errors[1] == pytest.approx((0.09757, 0.09757), 1e-1)

        errors = samples.error_magnitude_vector_at_sigma(sigma=1.0)

        assert errors == pytest.approx([0.0, 0.0], 1e-1)

        errors_instance = samples.error_instance_at_sigma(sigma=1.0)

        assert errors_instance.mock_class.one == pytest.approx(0.0, 1e-1)
        assert errors_instance.mock_class.two == pytest.approx(0.0, 1e-1)

        errors_instance = samples.error_instance_at_upper_sigma(sigma=3.0)

        assert errors_instance.mock_class.one == pytest.approx(0.09757, 1e-1)
        assert errors_instance.mock_class.two == pytest.approx(0.09757, 1e-1)

        errors_instance = samples.error_instance_at_lower_sigma(sigma=3.0)

        assert errors_instance.mock_class.one == pytest.approx(0.09757, 1e-1)
        assert errors_instance.mock_class.two == pytest.approx(0.09757, 1e-1)

    def test__unconverged_sample_size__uses_value_unless_fewer_samples(self):
        model = af.ModelMapper(mock_class_1=MockClassx4)

        log_likelihood_list = 4 * [0.0] + [1.0]
        weight_list = 4 * [0.0] + [1.0]

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=5 * [[]],
                log_likelihood_list=log_likelihood_list,
                log_prior_list=[1.0, 1.0, 1.0, 1.0, 1.0],
                weight_list=weight_list,

            ),
            unconverged_sample_size=2,
        )

        assert samples.pdf_converged is False
        assert samples.unconverged_sample_size == 2

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=5 * [[]],
                log_likelihood_list=log_likelihood_list,
                log_prior_list=[1.0, 1.0, 1.0, 1.0, 1.0],
                weight_list=weight_list,
            ),
            unconverged_sample_size=6,
        )

        assert samples.pdf_converged is False
        assert samples.unconverged_sample_size == 5

    def test__offset_vector_from_input_vector(self):
        model = af.ModelMapper(mock_class_1=MockClassx4)

        parameters = [
            [1.1, 2.1, 3.1, 4.1],
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.0],
            [1.0, 2.0, 3.0, 4.1],
        ]

        weight_list = [0.3, 0.2, 0.2, 0.2, 0.1]

        log_likelihood_list = list(map(lambda weight: 10.0 * weight, weight_list))

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(

                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        offset_values = samples.offset_vector_from_input_vector(
            input_vector=[1.0, 1.0, 2.0, 3.0]
        )

        assert offset_values == pytest.approx([0.0, 1.0, 1.0, 1.025], 1.0e-4)


    def test__vector_drawn_randomly_from_pdf(self):

        parameters = [
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [21.0, 22.0, 23.0, 24.0],
            [0.0, 1.0, 2.0, 3.0],
        ]

        model = af.ModelMapper(mock_class_1=MockClassx4)

        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=[1.0, 2.0, 3.0, 4.0, 5.0],
                log_prior_list=5 * [0.0],
                weight_list=[0.0, 0.0, 0.0, 1.0, 0.0],
            ),
        )

        vector = samples.vector_drawn_randomly_from_pdf()

        assert vector == [21.0, 22.0, 23.0, 24.0]

        instance = samples.instance_drawn_randomly_from_pdf()

        assert vector == [21.0, 22.0, 23.0, 24.0]

        assert instance.mock_class_1.one == 21.0
        assert instance.mock_class_1.two == 22.0
        assert instance.mock_class_1.three == 23.0
        assert instance.mock_class_1.four == 24.0

    def test__covariance_matrix(self):

        log_likelihood_list = list(range(3))

        weight_list = 3 * [0.1]

        parameters = [
            [2.0, 2.0],
            [1.0, 1.0],
            [0.0, 0.0],
        ]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=3 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.covariance_matrix() == pytest.approx(np.array([[1.0, 1.0], [1.0, 1.0]]), 1.0e-4)

        parameters = [
            [0.0, 2.0],
            [1.0, 1.0],
            [2.0, 0.0],
        ]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=3 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.covariance_matrix() == pytest.approx(np.array([[1.0, -1.0], [-1.0, 1.0]]), 1.0e-4)

        weight_list = [0.1, 0.2, 0.3]

        model = af.ModelMapper(mock_class=MockClassx2)
        samples = MockSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=log_likelihood_list,
                log_prior_list=10 * [0.0],
                weight_list=weight_list,
            ))

        assert samples.covariance_matrix() == pytest.approx(np.array([[0.90909, -0.90909], [-0.90909, 0.90909]]), 1.0e-4)

class MockNestSamples(af.NestSamples):

    def __init__(
            self,
            model,
            sample_list=None,
            total_samples=10,
            log_evidence=0.0,
            number_live_points=5,
    ):

        self.model = model

        if sample_list is None:

            sample_list = [
                Sample(
                    log_likelihood=log_likelihood,
                    log_prior=0.0,
                    weight=0.0
                )
                for log_likelihood
                in self.log_likelihood_list
            ]

        super().__init__(
            model=model,
            sample_list=sample_list
        )

        self._total_samples = total_samples
        self._log_evidence = log_evidence
        self._number_live_points = number_live_points


    @property
    def total_samples(self):
        return self._total_samples

    @property
    def log_evidence(self):
        return self._log_evidence

    @property
    def number_live_points(self):
        return self._number_live_points


class TestNestSamples:

    def test__samples_within_parameter_range(self, samples):
        model = af.ModelMapper(mock_class_1=MockClassx4)

        parameters = [
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [0.0, 1.0, 2.0, 3.0],
            [21.0, 22.0, 23.0, 24.0],
            [0.0, 1.0, 2.0, 3.0],
        ]

        samples = MockNestSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=parameters,
                log_likelihood_list=[1.0, 2.0, 3.0, 10.0, 5.0],
                log_prior_list=[0.0, 0.0, 0.0, 0.0, 0.0],
                weight_list=[1.0, 1.0, 1.0, 1.0, 1.0],
            ),
            total_samples=10,
            log_evidence=0.0,
            number_live_points=5,
        )

        samples_range = samples.samples_within_parameter_range(parameter_index=0, parameter_range=[-1.0, 100.0])

        assert len(samples_range.parameter_lists) == 5
        assert samples.parameter_lists[0] == samples_range.parameter_lists[0]

        samples_range = samples.samples_within_parameter_range(parameter_index=0, parameter_range=[1.0, 100.0])

        assert len(samples_range.parameter_lists) == 1
        assert samples_range.parameter_lists[0] == [21.0, 22.0, 23.0, 24.0]

        samples_range = samples.samples_within_parameter_range(parameter_index=2, parameter_range=[1.5, 2.5])

        assert len(samples_range.parameter_lists) == 4
        assert samples_range.parameter_lists[0] == [0.0, 1.0, 2.0, 3.0]
        assert samples_range.parameter_lists[1] == [0.0, 1.0, 2.0, 3.0]
        assert samples_range.parameter_lists[2] == [0.0, 1.0, 2.0, 3.0]
        assert samples_range.parameter_lists[3] == [0.0, 1.0, 2.0, 3.0]

    def test__acceptance_ratio_is_correct(self):
        model = af.ModelMapper(mock_class_1=MockClassx4)

        samples = MockNestSamples(
            model=model,
            sample_list=Sample.from_lists(
                model=model,
                parameter_lists=5 * [[]],
                log_likelihood_list=[1.0, 2.0, 3.0, 4.0, 5.0],
                log_prior_list=5 * [0.0],
                weight_list=5 * [0.0],
            ),
            total_samples=10,
            log_evidence=0.0,
            number_live_points=5,
        )

        assert samples.acceptance_ratio == 0.5
