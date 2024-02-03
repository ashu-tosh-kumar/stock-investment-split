from tabulate import tabulate

from src.models.financial_instruments import FinancialInstruments

MARGIN_DEVIATION = 0.01


def analyze_and_print_results(financial_instruments: FinancialInstruments, new_investment: float, results: list[float]) -> None:
    """Helper function to analyze and print helpful summary and/or warnings for final results

    Args:
        financial_instruments (FinancialInstruments): Model representing the portfolio
        new_investment (float): New investment to be made
        results (list[float]): Results of the optimizer containing suggested allocation
        of `new_investment` for various instruments
    """
    total_initial_investment: float = sum([investment.initial_investment for investment in financial_instruments.instruments])
    total_final_investment: float = total_initial_investment + new_investment

    allocation_data: list = [
        (
            instrument.identifier,  # Identifier
            ((100 * instrument.initial_investment) / total_initial_investment),  # Initial Investment Ratio
            100 * instrument.target_investment_ratio,  # Target Investment Ratio
            investment,  # Suggested Investment
            ((100 * (instrument.initial_investment + investment)) / total_final_investment),  # Final Ratio
        )
        for instrument, investment in zip(financial_instruments.instruments, results)
    ]

    print(f"Final allocation of investment of unit {new_investment} is as follows:")
    print(tabulate(allocation_data, headers=["Instrument", "Initial Investment %", "Target Investment %", "Suggested Investment", "Final Ratio"]))

    total_suggested_allocation: float = sum(results)
    if abs(total_suggested_allocation - new_investment) / (new_investment) > MARGIN_DEVIATION:
        print(
            f"Total suggested allocation is of unit {total_suggested_allocation} which is more than {MARGIN_DEVIATION*100}% different than investment amount {new_investment}"  # noqa: E501
        )

    print("Please manually verify the results as Mathematics can only aid you but can't absolve you!")
