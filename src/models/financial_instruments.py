from pydantic import BaseModel, validator


class FinancialInstrument(BaseModel):
    """Defines a financial instrument"""

    identifier: str  # Financial instrument name/symbol for unique identification
    initial_investment: float  # initial investment in your currency
    target_investment_ratio: float

    @validator("target_investment_ratio")
    def validate_non_negative_ratio(cls, value: float) -> float:
        """Custom validator to ensure that `target_investment_ratio` is non-negative

        Args:
            value (float): Value passed

        Raises:
            ValueError: Raised if value passed is negative

        Returns:
            float: Value returned after validation is successful
        """
        if value < 0:
            raise ValueError("Target investment ratio must be non-negative.")

        if value > 1:
            raise ValueError("Target investment ratio must be less than equal to 1.")

        return value


class FinancialInstruments(BaseModel):
    """Defines a list of financial instrument. Effectively it represents the
    portfolio"""

    instruments: list[FinancialInstrument]

    @validator("instruments")
    def validate_instruments(cls, instruments: list[FinancialInstrument]) -> list[FinancialInstrument]:
        """Custom validator to validate that sum of all ratios across all instruments is
        less than equal to `1`.

        Args:
            instruments (list[FinancialInstrument]): List of financial instruments
            passed

        Raises:
            ValueError: Raised if sum of all `target_investment_ratio` across all
            financial instruments is not less than equal to `1`

        Returns:
            list[FinancialInstrument]: List of financial instruments
            after validation is successful
        """
        # Validate that the sum of target_investment_ratio is less than equal to 1
        sum_ratios = sum(instrument.target_investment_ratio for instrument in instruments)
        if not (0 < sum_ratios <= 1.001):
            raise ValueError("Sum of target investment ratios must be less than equal to 1.")

        return instruments
