from math import floor

from tabulate import tabulate

from src.models.financial_instruments import FinancialInstruments

MARGIN_DEVIATION = 0.01


def analyze_and_print_results(financial_instruments: FinancialInstruments, new_investment: float, results: list[float], metadata: dict = None) -> None:
    """Helper function to analyze and print helpful summary and/or warnings for final results

    Args:
        financial_instruments (FinancialInstruments): Model representing the portfolio
        new_investment (float): New investment to be made
        results (list[float]): Results of the optimizer containing suggested allocation
        of `new_investment` for various instruments
        metadata (dict, optional): Additional metadata about the solution
    """
    total_initial_investment: float = sum([investment.initial_investment for investment in financial_instruments.instruments])
    total_final_investment: float = total_initial_investment + new_investment

    allocation_data: list = [
        (
            instrument.identifier,  # Identifier
            ((100 * instrument.initial_investment) / total_initial_investment),  # Initial Investment Ratio
            100 * instrument.target_investment_ratio,  # Target Investment Ratio
            investment,  # Suggested Investment
            ((100 * (instrument.initial_investment + investment)) / total_final_investment),  # Final %
        )
        for instrument, investment in zip(financial_instruments.instruments, results)
    ]

    print(f"Final allocation of investment of unit {new_investment} is as follows:")
    print(tabulate(allocation_data, headers=["Instrument", "Initial Investment %", "Target Investment %", "Suggested Investment", "Final %"]))

    total_suggested_allocation: float = sum(results)
    if abs(total_suggested_allocation - new_investment) / (new_investment) > MARGIN_DEVIATION:
        print(
            f"Total suggested allocation is of unit {total_suggested_allocation} which is more than {MARGIN_DEVIATION*100}% different than investment amount {new_investment}"  # noqa: E501
        )

    # Display additional metadata if available
    if metadata:
        _print_solution_metadata(metadata)

    print("Please manually verify the results as Mathematics can only aid you but can't absolve you!")


def sanitize_too_small_values(results: list[float], inplace: bool = False) -> list[float]:
    """Sanitizes and returns the list of results. Supports inplace as well as non in
    place changes in `results`

    - Takes `math.floor` of values to round off

    Args:
        results (list[float]): List of results

    Returns:
        list[float]: Returns a originally modified list if `inplace` is `True` and
        returns a new list of results after sanitizing
    """
    if inplace:
        for i in range(len(results)):
            results[i] = max(0, floor(results[i]))

        return results

    return [max(0, floor(result)) for result in results]


def _print_solution_metadata(metadata: dict) -> None:
    """Print solution metadata including comparison information."""
    print("\n" + "=" * 60)
    print("SOLUTION ANALYSIS")
    print("=" * 60)

    # Check if this is a comparison between analytical and numerical
    if "analytical_mse" in metadata and "numerical_mse" in metadata:
        print(f"Analytical MSE: {metadata['analytical_mse']:.6f}")
        print(f"Numerical MSE:  {metadata['numerical_mse']:.6f}")

        if metadata["analytical_mse"] <= metadata["numerical_mse"]:
            improvement = ((metadata["numerical_mse"] - metadata["analytical_mse"]) / metadata["numerical_mse"] * 100) if metadata["numerical_mse"] > 0 else 0
            print(f"Analytical solution is better by {improvement:.2f}%")
        else:
            print("Numerical solution performed better than analytical")

        if metadata.get("solutions_are_similar", False):
            print("Both solutions are very similar (difference < 0.01)")
        else:
            print(f"Max allocation difference: {metadata.get('max_allocation_difference', 0):.2f}")
            print(f"Avg allocation difference: {metadata.get('avg_allocation_difference', 0):.2f}")

    # Display analytical solution metadata if available
    if "analytical_metadata" in metadata:
        analytical_meta = metadata["analytical_metadata"]
        print("\nANALYTICAL SOLUTION DETAILS:")
        print(f"   • Unconstrained feasible: {'Yes' if analytical_meta.get('is_unconstrained_feasible', True) else 'No'}")
        if not analytical_meta.get("is_unconstrained_feasible", True):
            print(f"   • Constraint iterations: {analytical_meta.get('iterations', 0)}")
            constrained = analytical_meta.get("constrained_instruments", [])
            if constrained:
                print(f"   • Constrained instruments: {constrained}")
        print(f"   • Final MSE: {analytical_meta.get('final_mse', 0):.6f}")

    print("=" * 60)
