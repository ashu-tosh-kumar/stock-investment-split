import warnings
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
    use_smart_initial_guess: bool = True,
) -> np.ndarray:
    """Optimizer using `scipy.optimize.minimize` to minimize a the `error_function`

    Args:
        error_function (Callable[[FinancialInstruments, float], Callable[[np.ndarray],
        float]]): Error function that needs to be optimized
        financial_instruments (FinancialInstruments): Financial instruments model object
        new_investment (float): Amount of new investment that needs to be distributed
        method (ScipyOptimizeMinimizeMethods, optional): Method to be used for
        minimizing the `error_function`. Defaults to ScipyOptimizeMinimizeMethods.SLSQP.
        use_smart_initial_guess (bool): Whether to use smart initial guess based on
        analytical solution. Defaults to True.

    Returns:
        np.ndarray: Returns array of split of `new_investment` into initial financial
        instruments to achieve target ratio as close as possible

    Raises:
        ValueError: If inputs are invalid or optimization fails
    """

    # Validate inputs
    _validate_optimizer_inputs(financial_instruments, new_investment)

    def constraint_sum_equal_to_new_investment(x: np.ndarray) -> float:
        """Constraint: The sum of all elements of x must be equal to new_investment

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
    bounds = tuple((0, new_investment) for _ in range(num_investments))  # Bounds for each variable: 0 to `new_investment`

    # Generate initial guess
    if use_smart_initial_guess:
        x_0 = _generate_smart_initial_guess(financial_instruments, new_investment)
    else:
        equitable_distribution = new_investment // num_investments
        x_0 = np.asarray(
            [equitable_distribution] * (num_investments - 1) + [new_investment - (equitable_distribution * (num_investments - 1))]
        )  # Initial guess

    # Run optimization with multiple attempts if needed
    results = _optimize_with_fallback(error_function_callable, x_0, method, bounds, constraints, new_investment)

    # Validate results
    _validate_optimization_results(results, new_investment)

    return results.x


def _validate_optimizer_inputs(financial_instruments: FinancialInstruments, new_investment: float) -> None:
    """Validate inputs to the optimizer."""
    if new_investment <= 0:
        raise ValueError("New investment must be positive")

    if len(financial_instruments.instruments) == 0:
        raise ValueError("Must have at least one financial instrument")

    # Check for zero initial investments
    initial_investments = [inst.initial_investment for inst in financial_instruments.instruments]
    if any(inv < 0 for inv in initial_investments):
        raise ValueError("Initial investments cannot be negative")

    # Warn about zero initial investments
    if any(inv == 0 for inv in initial_investments):
        warnings.warn("Some instruments have zero initial investment. Results may be suboptimal.")

    # Check target ratios
    target_ratios = [inst.target_investment_ratio for inst in financial_instruments.instruments]
    if not np.isclose(sum(target_ratios), 1.0, atol=1e-6):
        raise ValueError("Target ratios must sum to 1.0")


def _generate_smart_initial_guess(financial_instruments: FinancialInstruments, new_investment: float) -> np.ndarray:
    """Generate a smart initial guess based on analytical solution."""
    try:
        # Import here to avoid circular imports
        from src.controller.analytical_solver import solve_analytically

        analytical_allocation, _ = solve_analytically(financial_instruments, new_investment)
        return np.array(analytical_allocation)
    except Exception:
        # Fallback to equal distribution if analytical solution fails
        warnings.warn("Failed to generate smart initial guess, using equal distribution")
        num_investments = len(financial_instruments.instruments)
        equitable_distribution = new_investment / num_investments
        return np.full(num_investments, equitable_distribution)


def _optimize_with_fallback(
    error_function_callable: Callable[[np.ndarray], float],
    x_0: np.ndarray,
    method: ScipyOptimizeMinimizeMethods,
    bounds: tuple,
    constraints: list,
    new_investment: float,
) -> scipy.optimize.OptimizeResult:
    """Run optimization with fallback strategies."""

    # First attempt with provided method
    results = scipy.optimize.minimize(error_function_callable, x_0, method=method.value, bounds=bounds, constraints=constraints)

    if results.success:
        return results

    # Fallback 1: Try with SLSQP if not already used
    if method != ScipyOptimizeMinimizeMethods.SLSQP:
        warnings.warn(f"Optimization with {method.value} failed, trying SLSQP")
        results = scipy.optimize.minimize(error_function_callable, x_0, method="SLSQP", bounds=bounds, constraints=constraints)
        if results.success:
            return results

    # Fallback 2: Try with different initial guess (equal distribution)
    warnings.warn("Trying optimization with equal distribution initial guess")
    num_investments = len(x_0)
    equal_x_0 = np.full(num_investments, new_investment / num_investments)
    results = scipy.optimize.minimize(error_function_callable, equal_x_0, method="SLSQP", bounds=bounds, constraints=constraints)

    if results.success:
        return results

    # If all attempts fail, return the last result (caller will handle the failure)
    warnings.warn("All optimization attempts failed")
    return results


def _validate_optimization_results(results: scipy.optimize.OptimizeResult, new_investment: float) -> None:
    """Validate optimization results."""
    if not results.success:
        warnings.warn(f"Optimization did not converge: {results.message}")

    # Check if solution satisfies constraints
    total_allocated = np.sum(results.x)
    if not np.isclose(total_allocated, new_investment, atol=1e-6):
        warnings.warn(f"Solution may not satisfy sum constraint: {total_allocated} != {new_investment}")

    # Check for negative values
    if np.any(results.x < -1e-10):
        warnings.warn("Solution contains negative allocations")

    # Clean up small negative values
    results.x = np.maximum(results.x, 0)
