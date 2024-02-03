from src.controller.error import mean_squared_error
from src.controller.scipy_optimizer import scipy_optimize_minimize
from src.controller.utils.results import sanitize_too_small_values
from src.models.financial_instruments import FinancialInstruments
from src.models.optimizers import ScipyOptimizeMinimizeMethods


def run(financial_instruments: FinancialInstruments, new_investment: float) -> list[float]:
    """Main function to run the optimizer and return results

    Args:
        financial_instruments (FinancialInstruments): Model representing the financial
        models
        new_investment (float): Amount of new investment to be made

    Returns:
        list[float]: List of investment in each financial instrument to be made. It is
        in the same order as instruments in `financial_instruments.instruments` list
    """
    # Define financial instruments and their weightage
    print("Optimizing the MSE to compute optimal allocation. Sit tight!")
    financial_instruments_target_investment_array = scipy_optimize_minimize(
        mean_squared_error, financial_instruments, new_investment, method=ScipyOptimizeMinimizeMethods.SLSQP
    )

    # Sanitize too small values
    results_list = list(financial_instruments_target_investment_array)
    sanitize_too_small_values(results_list, inplace=True)

    return results_list
