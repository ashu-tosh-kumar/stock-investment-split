from test.mocks import DUMMY_FINANCIAL_INSTRUMENTS, PropertyMock
from unittest.mock import Mock

import numpy as np

from src.controller.scipy_optimizer import scipy_optimize_minimize

SCIPY = "src.controller.scipy_optimizer.scipy"


class TestScipyOptimizeMinimize:
    def test_scipy_optimize_minimize_should_optimize(self, mocker):
        dummy_error_function = Mock()
        dummy_new_investment = 30
        expected_value = np.asarray([10.0, 10.0, 10.0])
        stub_scipy = mocker.patch(SCIPY)
        stub_scipy.optimize.minimize.return_value = PropertyMock(x=expected_value)

        actual_value = scipy_optimize_minimize(dummy_error_function, DUMMY_FINANCIAL_INSTRUMENTS, dummy_new_investment)

        assert np.array_equal(expected_value, actual_value)
