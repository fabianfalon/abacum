"""Circles URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import (
    FileUploadAPIView,
    TransactionViewSet,
    TransactionBalanceByAccount,
    TransactionGetFullYearBalanceByAccount,
    TransactionGetMonthlyBalanceForSpecificMonthlyAndSpecificAccount,
    TransactionGetMonthlyBalanceForSpecificMonthByAccount
)

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transactions")


urlpatterns = [
    path("", include(router.urls)),
    path("upload/", FileUploadAPIView.as_view(), name="upload"),
    path("balance/<str:account>/", TransactionBalanceByAccount.as_view()),
    path(
        "balance/full-year/by-account/",
        TransactionGetFullYearBalanceByAccount.as_view(),
    ),
    path(
        "balance/monthly/<int:month>/account/<str:account>/",
        TransactionGetMonthlyBalanceForSpecificMonthlyAndSpecificAccount.as_view(),
    ),
    path(
        "balance/monthly/<int:month>/account/",
        TransactionGetMonthlyBalanceForSpecificMonthByAccount.as_view(),
    ),
]
