from datetime import datetime

import pytest

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


@pytest.mark.django_db
class TestViews:
    URL_BASE = "http://localhost:8000/"
    ACCOUNT = "1111"

    def test_get_transactions(self, client, populate_transactions):
        response = client.get(f"{self.URL_BASE}api/transactions/")
        assert response.status_code == 200
        assert response.json().get("count") == 3

    def test_get_balance_by_year_by_account(self, client, populate_transactions):
        response = client.get(
            f"{self.URL_BASE}api/balance/{self.ACCOUNT}/?frequency=year"
        )
        assert response.status_code == 200
        assert response.json().get("results") == [{"account": "1111", "balance": "300.00"}]

    def test_get_balance_by_month_by_account(self, client, populate_transactions):
        expected = [
            {"account": "1111", "balance": "100.00", "date": "2020-12"},
            {"account": "1111", "balance": "100.00", "date": "2020-11"},
            {"account": "1111", "balance": "100.00", "date": "2020-10"},
        ]
        response = client.get(
            f"{self.URL_BASE}api/balance/{self.ACCOUNT}/?frequency=monthly"
        )
        assert response.status_code == 200
        assert response.json().get("results") == expected

    @pytest.mark.parametrize(
        'frequency, status_code', [('TEST', 400), ('MONTH', 400), ('MONTHLY', 200), (None, 400)]
    )
    def test_get_balance_by_fail_frequency(self, client, populate_transactions, frequency, status_code):
        response = client.get(
            f"{self.URL_BASE}api/balance/{self.ACCOUNT}/?frequency={frequency}"
        )
        assert response.status_code == status_code

    def test_get_balance_full_year_by_account(self, client, populate_transactions):

        response = client.get(
            f"{self.URL_BASE}api/balance/full-year/by-account/"
        )
        assert response.status_code == 200
        assert response.json().get("results") == [{'account': '1111', 'balance': '300.00'}]

    def test_get_balance_full_year_by_account(self, client, populate_transactions):

        response = client.get(
            f"{self.URL_BASE}api/balance/full-year/by-account/"
        )
        assert response.status_code == 200
        assert response.json().get("results") == [{'account': '1111', 'balance': '300.00'}]

    def test_get_balance_monthly_by_specific_month_and_specific_account(self, client, populate_transactions):
        expected = [{'account': '1111', 'balance': '100.00', 'date': '2020-10'}]
        response = client.get(
            f"{self.URL_BASE}api/balance/monthly/10/account/1111/"
        )
        assert response.status_code == 200
        assert response.json().get("results") == expected

    def test_get_balance_by_month(self, client, populate_transactions):
        expected = [{'account': '1111', 'balance': '100.00', 'date': '2020-11'}]
        response = client.get(
            f"{self.URL_BASE}api/balance/monthly/11/account/"
        )
        assert response.status_code == 200
        assert response.json().get("results") == expected
