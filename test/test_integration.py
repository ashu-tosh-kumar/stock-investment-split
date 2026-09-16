from test.mocks import DUMMY_FINANCIAL_INSTRUMENTS

import pytest

from src.controller.run import run


@pytest.mark.integration
class TestStockInvestmentSplit:
    def test_stock_investment_split(self, snapshot):
        new_investment = 30

        actual_value, metadata = run(DUMMY_FINANCIAL_INSTRUMENTS, new_investment, method="numerical")

        assert snapshot == actual_value
