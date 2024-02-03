from typing import Callable

import numpy as np

from src.models.financial_instruments import FinancialInstruments


def mean_squared_error(financial_instruments: FinancialInstruments, new_investment: float) -> Callable[[np.ndarray], float]:
    """Closure that returns a callable function that when passed with `N_i` values i.e.
    the target investment ratio for financial instruments returns the Mean Squared Error
    (`MSE`)

    Equation: `(1/n)sum_(i=1)^n ((I_i + N_i)/(SI + SN) - T_i)^2`
    Use https://asciimath.org to render above equation

    Args:
        financial_instruments (FinancialInstruments): Model representing all financial
        instruments part of the portfolio
        new_investment (float): Total amount of new investment to be made

    Returns:
        Callable[[np.ndarray], float]: Returns a callable function that takes `N_i` and
        returns `MSE`
    """
    num_instruments: int = len(financial_instruments.instruments)
    I_i: np.ndarray = np.asarray([instrument.initial_investment for instrument in financial_instruments.instruments])  # /NOSONAR
    SI: float = sum([instrument.initial_investment for instrument in financial_instruments.instruments])
    SN: float = new_investment
    T_i: np.ndarray = np.asarray([instrument.target_investment_ratio for instrument in financial_instruments.instruments])  # /NOSONAR

    def mean_squared_error_inner(N_i: np.ndarray) -> float:  # /NOSONAR
        """Inner function that actually computes the MSE and returns the same

        Args:
            N_i (np.ndarray): Array of new investment allocated to each financial
            instrument

        Returns:
            float: MSE
        """
        I_i_plus_N_i = np.add(I_i, N_i)  # /NOSONAR
        SI_plus_SN = SI + SN  # /NOSONAR
        I_i_plus_N_i_divided_by_SI_plus_SN = np.divide(I_i_plus_N_i, SI_plus_SN)  # /NOSONAR
        se_array = np.power(np.subtract(I_i_plus_N_i_divided_by_SI_plus_SN, T_i), 2)
        mse: float = np.sum(se_array) / num_instruments
        return mse

    return mean_squared_error_inner
