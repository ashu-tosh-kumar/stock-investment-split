from test.mocks import FINANCIAL_INSTRUMENTS_MODELS

from src.models.financial_instruments import FinancialInstrument, FinancialInstruments


class TestFinancialInstrument:
    def test_financial_instrument_model(self):
        dummy_identifier = "INFOSYS"
        dummy_initial_investment = 30
        dummy_target_investment_ratio = 0.34

        financial_instrument = FinancialInstrument(
            identifier=dummy_identifier, initial_investment=dummy_initial_investment, target_investment_ratio=dummy_target_investment_ratio
        )

        assert dummy_identifier == financial_instrument.identifier
        assert dummy_initial_investment == financial_instrument.initial_investment
        assert round(dummy_target_investment_ratio, 2) == round(financial_instrument.target_investment_ratio, 2)


class TestFinancialInstruments:
    def test_financial_instruments(self):
        financial_instruments_model = FinancialInstruments(instruments=FINANCIAL_INSTRUMENTS_MODELS)

        assert FINANCIAL_INSTRUMENTS_MODELS == financial_instruments_model.instruments
