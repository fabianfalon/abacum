import calendar

from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear


class Transactions(models.Model):

    account = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )

    class Meta:
        ordering = ["created"]
        db_table = "transactions"
        unique_together = ("account", "date", "amount")

    def __str__(self):
        return f"transaction {self.id} {self.account}"

    @classmethod
    def get_balance_by_frequency(cls, account, frequency):
        if frequency == "monthly":
            return (
                cls.objects.filter(account=account)
                .annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(balance=Sum("amount"))
                .values("account", "month", "balance")
                .order_by("-month")
            )
        elif frequency == "year":
            return (
                cls.objects.filter(account=account)
                .annotate(year=TruncYear("date"))
                .values("year")
                .annotate(balance=Sum("amount"))
                .values("account", "balance")
                .order_by("-year")
            )

    @classmethod
    def get_full_year_balance_by_account(cls):
        return (
            cls.objects.values("account")
            .order_by("account")
            .annotate(balance=Sum("amount"))
        )

    @classmethod
    def get_monthly_balance_by_month_by_account(cls, month, account):
        days = calendar.monthrange(2020, month)
        start_date = f"2020-{month}-{days[0]}"
        end_date = f"2020-{month}-{days[1]}"

        return (
            cls.objects.filter(account=account, date__range=[start_date, end_date])
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(balance=Sum("amount"))
            .values("account", "month", "balance")
            .order_by("-month")
        )

    @classmethod
    def get_balance_by_month(cls, month):
        days = calendar.monthrange(2020, month)
        start_date = f"2020-{month}-{days[0]}"
        end_date = f"2020-{month}-{days[1]}"

        return (
            cls.objects.filter(date__range=[start_date, end_date])
            .annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(balance=Sum("amount"))
            .values("account", "month", "balance")
            .order_by("-month")
        )
