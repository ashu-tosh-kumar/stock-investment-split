from typing import Literal, Optional, Tuple

from src.controller.analytical_solver import solve_analytically
from src.controller.error import mean_squared_error
from src.controller.scipy_optimizer import scipy_optimize_minimize
from src.controller.utils.results import sanitize_too_small_values
from src.models.financial_instruments import FinancialInstruments
from src.models.optimizers import ScipyOptimizeMinimizeMethods


def run(
    financial_instruments: FinancialInstruments, new_investment: float, method: Literal["analytical", "numerical", "both"] = "both"
) -> Tuple[list[float], Optional[dict]]:
    """Main function to run the optimizer and return results

    Args:
        financial_instruments (FinancialInstruments): Model representing the financial
        instruments
        new_investment (float): Amount of new investment to be made
        method (Literal["analytical", "numerical", "both"]): Solution method to use.
            - "analytical": Use exact analytical solution
            - "numerical": Use numerical optimization
            - "both": Use both and compare results (default)

    Returns:
        Tuple containing:
        - list[float]: List of investment in each financial instrument to be made.
          It is in the same order as instruments in `financial_instruments.instruments` list
        - Optional[dict]: Metadata about the solution (comparison info if method="both")
    """
    if method == "analytical":
        print("Computing optimal allocation using analytical solution...")
        allocation, metadata = solve_analytically(financial_instruments, new_investment)
        sanitize_too_small_values(allocation, inplace=True)
        return allocation, metadata

    elif method == "numerical":
        print("Optimizing the MSE to compute optimal allocation using numerical methods. Sit tight!")
        financial_instruments_target_investment_array = scipy_optimize_minimize(
            mean_squared_error, financial_instruments, new_investment, method=ScipyOptimizeMinimizeMethods.SLSQP, use_smart_initial_guess=True
        )
        results_list = list(financial_instruments_target_investment_array)
        sanitize_too_small_values(results_list, inplace=True)
        return results_list, None

    else:  # method == "both"
        print("Computing optimal allocation using both analytical and numerical methods for comparison...")

        # Get analytical solution
        analytical_allocation, analytical_metadata = solve_analytically(financial_instruments, new_investment)

        # Get numerical solution
        numerical_allocation_array = scipy_optimize_minimize(
            mean_squared_error, financial_instruments, new_investment, method=ScipyOptimizeMinimizeMethods.SLSQP, use_smart_initial_guess=True
        )
        numerical_allocation = list(numerical_allocation_array)

        # Sanitize both results
        sanitize_too_small_values(analytical_allocation, inplace=True)
        sanitize_too_small_values(numerical_allocation, inplace=True)

        # Compare solutions
        comparison_metadata = _compare_solutions(analytical_allocation, numerical_allocation, financial_instruments, new_investment, analytical_metadata)

        # Return the better solution (lower MSE)
        if comparison_metadata["analytical_mse"] <= comparison_metadata["numerical_mse"]:
            print("Analytical solution is optimal")
            return analytical_allocation, comparison_metadata
        else:
            print("Numerical solution is better")
            return numerical_allocation, comparison_metadata


def run_simple(financial_instruments: FinancialInstruments, new_investment: float) -> list[float]:
    """
    Backward compatibility function that returns only the results list.

    This function maintains the old interface for existing code that expects
    just the results without metadata.

    Args:
        financial_instruments: Portfolio of financial instruments
        new_investment: Amount of new investment to allocate

    Returns:
        List of optimal allocations for each instrument
    """
    results, _ = run(financial_instruments, new_investment, method="both")
    return results


def _compare_solutions(
    analytical_allocation: list[float],
    numerical_allocation: list[float],
    financial_instruments: FinancialInstruments,
    new_investment: float,
    analytical_metadata: dict,
) -> dict:
    """Compare analytical and numerical solutions."""

    def calculate_mse(allocation: list[float]) -> float:
        """Calculate MSE for given allocation."""
        initial_investments = [inst.initial_investment for inst in financial_instruments.instruments]
        target_ratios = [inst.target_investment_ratio for inst in financial_instruments.instruments]
        total_initial = sum(initial_investments)
        total_final = total_initial + new_investment

        final_investments = [initial + alloc for initial, alloc in zip(initial_investments, allocation)]
        final_ratios = [final / total_final for final in final_investments]
        squared_errors = [(final_ratio - target_ratio) ** 2 for final_ratio, target_ratio in zip(final_ratios, target_ratios)]
        return sum(squared_errors) / len(squared_errors)

    analytical_mse = calculate_mse(analytical_allocation)
    numerical_mse = calculate_mse(numerical_allocation)

    # Check if solutions are significantly different
    allocation_diff = [abs(a - n) for a, n in zip(analytical_allocation, numerical_allocation)]
    max_diff = max(allocation_diff)
    avg_diff = sum(allocation_diff) / len(allocation_diff)

    return {
        "analytical_allocation": analytical_allocation,
        "numerical_allocation": numerical_allocation,
        "analytical_mse": analytical_mse,
        "numerical_mse": numerical_mse,
        "mse_improvement": (numerical_mse - analytical_mse) / numerical_mse if numerical_mse > 0 else 0,
        "max_allocation_difference": max_diff,
        "avg_allocation_difference": avg_diff,
        "solutions_are_similar": max_diff < 0.01,  # Less than 1 unit difference
        "analytical_metadata": analytical_metadata,
    }
