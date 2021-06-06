import csv
import io
from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from transactions.models import Transactions
from transactions.serializers import (
    FileUploadSerializer,
    TransactionByFrequencySerializer,
    TransactionModelSerializer,
)


class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="Upload file...",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        decoded_file = file.read().decode()

        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)

        # This skips the first row of the CSV file.
        next(reader)

        for row in reader:
            transaction, _ = Transactions.objects.get_or_create(
                account=row[1],
                date=datetime.strptime(row[0], "%Y-%m-%d"),
                defaults={"amount": row[2]},
            )
            print(transaction)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Transaction view set."""

    queryset = Transactions.objects.all()
    serializer_class = TransactionModelSerializer


class TransactionBalanceByAccount(generics.GenericAPIView, ListModelMixin):
    serializer_class = TransactionByFrequencySerializer
    queryset = Transactions.objects.all()

    frequency = openapi.Parameter(
        "frequency (year / monthly)",
        openapi.IN_QUERY,
        required=False,
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        operation_description="Return accounts grouped by year o monthly",
        operation_summary="Return accounts grouped by year o monthly",
        manual_parameters=[frequency],
        responses={
            200: TransactionByFrequencySerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        account = kwargs.get("account")
        frequency = self.request.GET.get("frequency", None)
        frequency = frequency.lower() if frequency else None

        if not frequency or frequency not in ["year", "monthly"]:
            return Response(
                "Frequency field error, wrong value",
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.queryset = Transactions.get_balance_by_frequency(account, frequency)
        return self.list(request, *args, **kwargs)


class TransactionGetFullYearBalanceByAccount(generics.GenericAPIView, ListModelMixin):
    serializer_class = TransactionByFrequencySerializer
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        operation_description="Get a full year balance by account",
        operation_summary="Get a full year balance by account",
        responses={
            200: TransactionByFrequencySerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        self.queryset = Transactions.get_full_year_balance_by_account()
        return self.list(request, *args, **kwargs)


class TransactionGetMonthlyBalanceForSpecificMonthlyAndSpecificAccount(
    generics.GenericAPIView, ListModelMixin
):
    serializer_class = TransactionByFrequencySerializer
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        operation_description="Get the monthly balance for a specific month and a specific account",
        operation_summary="Get the monthly balance for a specific month and a specific account",
        responses={
            200: TransactionByFrequencySerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        month = kwargs.get("month", 13)
        if int(month) > 12 or int(month) < 1:
            return Response(
                "Error, you are entering an incorrect or out of range month",
                status=status.HTTP_400_BAD_REQUEST,
            )

        account = kwargs.get("account")
        self.queryset = Transactions.get_monthly_balance_by_month_by_account(month, account)
        return self.list(request, *args, **kwargs)


class TransactionGetMonthlyBalanceForSpecificMonthByAccount(
    generics.GenericAPIView, ListModelMixin
):
    serializer_class = TransactionByFrequencySerializer
    queryset = Transactions.objects.all()

    @swagger_auto_schema(
        operation_description="Get the monthly balance for a specific month by account ",
        operation_summary="Get the monthly balance for a specific month by account ",
        responses={
            200: TransactionByFrequencySerializer(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        month = kwargs.get("month", None)
        if int(month) > 12 or int(month) < 1:
            return Response(
                "Error, you are entering an incorrect or out of range month",
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.queryset = Transactions.get_monthly_balance_by_month_by_account(month)
        return self.list(request, *args, **kwargs)

