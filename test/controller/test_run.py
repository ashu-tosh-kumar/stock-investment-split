from test.mocks import DUMMY_FINANCIAL_INSTRUMENTS

import numpy as np

from src.controller.run import run

SCIPY_OPTIMIZE_MINIMIZE = "src.controller.run.scipy_optimize_minimize"
SANITIZE_TOO_SMALL_VALUES = "src.controller.run.sanitize_too_small_values"


class TestRun:
    def test_run_should_return_expected_results(self, mocker):
        dummy_new_investment = 30
        dummy_financial_instruments_target_investment_array = np.asarray([10.0, 10.0, 10.0])
        mocker.patch(SCIPY_OPTIMIZE_MINIMIZE, return_value=dummy_financial_instruments_target_investment_array)
        mocker.patch(SANITIZE_TOO_SMALL_VALUES, side_effect=lambda *args, **kwargs: None)
        expected_value = list(dummy_financial_instruments_target_investment_array)

        actual_value = run(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment)

        assert expected_value == actual_value

    def test_run_should_sanitize_results(self, mocker):
        dummy_new_investment = 30
        dummy_financial_instruments_target_investment_array = np.asarray([10.0, 10.0, 10.0])
        mocker.patch(SCIPY_OPTIMIZE_MINIMIZE, return_value=dummy_financial_instruments_target_investment_array)
        spy_sanitize_too_small_values = mocker.patch(SANITIZE_TOO_SMALL_VALUES)

        run(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment)

        spy_sanitize_too_small_values.assert_called_once_with(list(dummy_financial_instruments_target_investment_array), inplace=True)
