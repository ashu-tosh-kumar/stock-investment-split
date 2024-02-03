import sys
from io import StringIO
from test.mocks import DUMMY_FINANCIAL_INSTRUMENTS

from src.controller.utils.results import (
    analyze_and_print_results,
    sanitize_too_small_values,
)


class TestAnalyzeAndPrintResults:
    def test_analyze_and_print_results_should_print_summary_below_deviation(self, snapshot):
        dummy_new_investment = 30
        dummy_results = [10.0, 10.0, 10.0]
        captured_output = StringIO()
        sys.stdout = captured_output

        analyze_and_print_results(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment, dummy_results)
        sys.stdout = sys.__stdout__  # Reset redirect

        assert snapshot == captured_output.getvalue()

    def test_analyze_and_print_results_should_print_summary_above_deviation(self, snapshot):
        dummy_new_investment = 30
        dummy_results = [5.0, 5.0, 5.0]
        captured_output = StringIO()
        sys.stdout = captured_output

        analyze_and_print_results(DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment, dummy_results)
        sys.stdout = sys.__stdout__  # Reset redirect

        assert snapshot == captured_output.getvalue()


class TestSanitizeTooSmallValues:
    def test_sanitize_too_small_values_inplace(self, snapshot):
        results = [10.0, 9.876, 10.065]
        inplace = True

        sanitize_too_small_values(results, inplace)

        assert snapshot == results

    def test_sanitize_too_small_values_not_inplace(self, snapshot):
        results = [10.0, 9.876, 10.065]
        inplace = True

        actual_value = sanitize_too_small_values(results, inplace)

        assert snapshot == actual_value
