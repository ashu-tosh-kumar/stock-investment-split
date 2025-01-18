import sys

from src.controller.run import run
from src.controller.utils.results import analyze_and_print_results
from src.models.financial_instruments import FinancialInstrument, FinancialInstruments

SYS_EXIT_ERROR_VALUE: int = 1

if __name__ == "__main__":
    financial_instruments_identifier_msg: str = "Please add identifier/names of financial instruments separated by comma(,)\n"
    financial_instruments_identifier_list: list[str] = [identifier.strip() for identifier in input(financial_instruments_identifier_msg).split(",")]

    financial_instruments_initial_investment_msg: str = "Please add initial investment (all in same currency) of financial instruments separated by comma(,)\n"
    financial_instruments_initial_investment_list: list[float] = list(map(float, input(financial_instruments_initial_investment_msg).split(",")))

    new_investment: float = int(input("How much money do you want to invest?\n"))

    financial_instruments_target_investment_ratio_msg: str = (
        "Please add target investment ratio (between 0 and 1) of financial instruments separated by comma(,)\n"
    )
    financial_instruments_target_investment_ratio_list: list[float] = list(map(float, input(financial_instruments_target_investment_ratio_msg).split(",")))

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
