from unittest.mock import MagicMock, Mock

from src.models.financial_instruments import FinancialInstrument, FinancialInstruments

_financial_instrument_list = [
    {"identifier": "INFOSYS", "initial_investment": 30, "target_investment_ratio": 0.33},
    {"identifier": "", "initial_investment": 50, "target_investment_ratio": 0.33},
    {"identifier": "", "initial_investment": 20, "target_investment_ratio": 0.34},
]
_financial_instruments_models = [FinancialInstrument(**financial_instrument_dict) for financial_instrument_dict in _financial_instrument_list]
DUMMY_FINANCIAL_INSTRUMENTS = FinancialInstruments(instruments=_financial_instruments_models)


class PropertyMock(Mock):
    """
    A mock intended to be used as a property, or other descriptor, on a class.
    `PropertyMock` provides `__get__` and `__set__` methods so you can specify
    a return value when it is fetched.

    Fetching a `PropertyMock` instance from an object calls the mock, with
    no args. Setting it calls the mock with the value being set.
    """

    def _get_child_mock(self, /, **kwargs):
        return MagicMock(**kwargs)

    def __get__(self, obj, obj_type=None):
        return self()

    def __set__(self, obj, val):
        self(val)
