from src.models.financial_instruments import FinancialInstrument, FinancialInstruments

_financial_instrument_list = [
    {"identifier": "INFOSYS", "initial_investment": 30, "target_investment_ratio": 0.33},
    {"identifier": "", "initial_investment": 50, "target_investment_ratio": 0.33},
    {"identifier": "", "initial_investment": 20, "target_investment_ratio": 0.34},
]
_financial_instruments_models = [FinancialInstrument(**financial_instrument_dict) for financial_instrument_dict in _financial_instrument_list]
DUMMY_FINANCIAL_INSTRUMENTS = FinancialInstruments(instruments=_financial_instruments_models)
