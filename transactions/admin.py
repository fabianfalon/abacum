"""User models admin."""

# Django
from django.contrib import admin

# Models
from transactions.models import Transactions


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    """Transaction model admin."""

    list_display = ("id", "account", "date", "amount")
    list_filter = ("account",)
