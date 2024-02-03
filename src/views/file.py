import sys

from src.controller.run import run
from src.controller.utils.results import analyze_and_print_results
from src.models.financial_instruments import FinancialInstrument, FinancialInstruments

# Example taken from `README` file
FINANCIAL_INSTRUMENT_NAMES: list[str] = ["INFOSYS", "TCS", "WIPRO"]  # modify the list here
FINANCIAL_INSTRUMENTS_INITIAL_INVESTMENT: list[float] = [30, 50, 20]  # modify the list here
NEW_INVESTMENT: float = 30  # modify the value here
FINANCIAL_INSTRUMENTS_TARGET_INVESTMENT_RATIO: list[float] = [0.33, 0.33, 0.34]  # modify the list here. Note it's a ratio and not percentage

SYS_EXIT_ERROR_VALUE: int = 1

if __name__ == "__main__":
    financial_instruments_identifier_list: list[str] = FINANCIAL_INSTRUMENT_NAMES
    financial_instruments_initial_investment_list: list[float] = FINANCIAL_INSTRUMENTS_INITIAL_INVESTMENT
    new_investment: float = NEW_INVESTMENT
    financial_instruments_target_investment_ratio_list: list[float] = FINANCIAL_INSTRUMENTS_TARGET_INVESTMENT_RATIO

    if len(financial_instruments_identifier_list) != len(financial_instruments_initial_investment_list):
        print(
            f"No. of financial instruments: {len(financial_instruments_identifier_list)} should match no. of initial investments: {len(financial_instruments_initial_investment_list)}"  # noqa: E501
        )
        sys.exit(SYS_EXIT_ERROR_VALUE)

    financial_instruments_list: list[FinancialInstrument] = []
    for identifier, initial_investment, target_investment_ratio in zip(
        financial_instruments_identifier_list, financial_instruments_initial_investment_list, financial_instruments_target_investment_ratio_list
    ):
        financial_instruments_list.append(
            FinancialInstrument(**{"identifier": identifier, "initial_investment": initial_investment, "target_investment_ratio": target_investment_ratio})
        )

    # Create models
    financial_instruments = FinancialInstruments(instruments=financial_instruments_list)

    results: list[float] = run(financial_instruments, new_investment)
    analyze_and_print_results(financial_instruments, new_investment, results)
