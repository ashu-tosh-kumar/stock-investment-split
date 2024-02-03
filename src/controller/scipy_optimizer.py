from typing import Callable

import numpy as np
import scipy

from src.models.financial_instruments import FinancialInstruments
from src.models.optimizers import ScipyOptimizeMinimizeMethods


def scipy_optimize_minimize(
    error_function: Callable[[FinancialInstruments, float], Callable[[np.ndarray], float]],
    financial_instruments: FinancialInstruments,
    new_investment: float,
    method: ScipyOptimizeMinimizeMethods = ScipyOptimizeMinimizeMethods.SLSQP,
) -> np.ndarray:
    """Optimizer using `scipy.optimize.minimize` to minimize a the `error_function`

    Args:
        error_function (Callable[[FinancialInstruments, float], Callable[[np.ndarray],
        float]]): Error function that needs to be optimized
        financial_instruments (FinancialInstruments): Financial instruments model object
        new_investment (float): Amount of new investment that needs to be distributed
        method (ScipyOptimizeMinimizeMethods, optional): Method to be used for
        minimizing the `error_function`. Defaults to ScipyOptimizeMinimizeMethods.SLSQP.

    Returns:
        np.ndarray: Returns array of split of `new_investment` into initial financial
        instruments to achieve target ratio as close as possible
    """

    def constraint_sum_equal_to_new_investment(x: np.ndarray) -> float:
        """Constraint: The sum of all elements of x must be equal to 1

        Args:
            x (np.ndarray): Array of values

        Returns:
            float: Returns if constrained is satisfied or not
        """
        return x.sum() - new_investment

    num_investments: int = len(financial_instruments.instruments)
    error_function_callable: Callable[[np.ndarray], float] = error_function(financial_instruments, new_investment)
    constraints = [
        {"type": "eq", "fun": constraint_sum_equal_to_new_investment},  # Equality constraint: sum of elements equals `new_investment`
    ]
    bounds = tuple((0, new_investment) for _ in range(num_investments))  # Bounds for each variable: 0 to `new_investment
    equitable_distribution = new_investment // num_investments
    x_0 = np.asarray([equitable_distribution] * (num_investments - 1) + [new_investment - (equitable_distribution * (num_investments - 1))])  # Initial guess

    results: scipy.optimize.OptimizeResult = scipy.optimize.minimize(error_function_callable, x_0, method=method.value, bounds=bounds, constraints=constraints)
    return results.x
