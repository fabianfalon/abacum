"""Transactions tests."""
import pytest
from datetime import datetime

# Model
from transactions.models import Transactions

# Factory
from transactions.tests.factories import TransactionsFactory


@pytest.fixture
def populate_transactions():

    TransactionsFactory.create(
        account="1111",
        amount=100,
        date=datetime.strptime("2020-10-20", "%Y-%m-%d"),
    )

    TransactionsFactory.create(
        account="1111",
        amount=100,
        date=datetime.strptime("2020-11-20", "%Y-%m-%d"),
    )
    TransactionsFactory.create(
        account="1111",
        amount=100,
        date=datetime.strptime("2020-12-20", "%Y-%m-%d"),
    )
    TransactionsFactory.create(
        account="2222",
        amount=100,
        date=datetime.strptime("2020-12-20", "%Y-%m-%d"),
    )


@pytest.mark.django_db
class TestTransaction:
    """Transaction model test case."""

    def test_get_balance_by_year_frequency(self, populate_transactions):

        result = Transactions.get_balance_by_frequency("1111", "year")
        result = list(result)
        assert result[0].get("balance") == 300
        assert result[0].get("account") == "1111"

    def test_get_balance_by_monthly_frequency(self, populate_transactions):

        result = Transactions.get_balance_by_frequency("1111", "monthly")
        result = list(result)

        assert result[0].get("account") == "1111"
        assert result[0].get("balance") == 100

        assert result[1].get("account") == "1111"
        assert result[1].get("balance") == 100

        assert result[2].get("account") == "1111"
        assert result[2].get("balance") == 100

    def test_get_full_year_balance_by_account(self, populate_transactions):

        result = Transactions.get_full_year_balance_by_account()
        result = list(result)

        expected = [
            {"account": "1111", "balance": 300},
            {"account": "2222", "balance": 100},
        ]
        assert result == expected

    def test_get_balance_monthly_by_specific_month_and_specific_account(self, populate_transactions):

        result = Transactions.get_monthly_balance_by_month_by_account(12, "2222")
        result = list(result)

        expected = [
            {"account": "2222", "month": datetime(2020, 12, 1).date(), "balance": 100},
        ]
        assert result == expected

    def test_get_balance_by_month(self, populate_transactions):

        result = Transactions.get_balance_by_month(12)
        result = list(result)
        expected = [
            {"account": "1111", "month": datetime(2020, 12, 1).date(), "balance": 100},
            {"account": "2222", "month": datetime(2020, 12, 1).date(), "balance": 100}
        ]
        assert result == expected
        assert len(result) == 2
