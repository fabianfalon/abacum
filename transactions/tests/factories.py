import factory
from datetime import datetime
from factory.fuzzy import FuzzyText, FuzzyDate, FuzzyDecimal

from transactions.models import Transactions


class TransactionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transactions

    account = FuzzyText(length=50)
    date = FuzzyDate(start_date=datetime.strptime("2020-10-10", "%Y-%m-%d").date())
    amount = FuzzyDecimal(low=100, high=10000, precision=2)
