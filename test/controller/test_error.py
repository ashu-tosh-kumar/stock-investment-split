from test.mocks import DUMMY_FINANCIAL_INSTRUMENTS

import numpy as np
import pytest

from src.controller.error import mean_squared_error


class TestMeanSquaredError:
    def test_mean_squared_error_should_return_expected_callable(self):
        dummy_new_investment = 30

        actual_value = mean_squared_error(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment)
        N_i = np.asarray([10.0, 10.0, 10.0])  # /NOSONAR

        assert actual_value(N_i)  # no errors expected

    @pytest.mark.parametrize(
        "N_i",
        [
            (np.asarray([10.0, 10.0, 10.0]),),
            (np.asarray([53.37979411, 79.53647717, 86.27138012]),),
            (np.asarray([-3.38749768, -76.40340437, 49.0709542]),),
        ],
        ids=["example_1", "example_2", "example_3"],
    )
    def test_mean_squared_error_returned_callable_should_return_expected_values(self, N_i, snapshot):  # /NOSONAR
        dummy_new_investment = 30

        _callable = mean_squared_error(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment)
        actual_value = _callable(N_i)

        assert snapshot == actual_value
