from rest_framework import serializers
from transactions.models import Transactions


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ("file",)


class TransactionModelSerializer(serializers.ModelSerializer):
    """Transaction model serializer."""

    class Meta:
        """Meta class."""

        model = Transactions
        fields = "__all__"


class TransactionByFrequencySerializer(serializers.Serializer):
    """TransactionByFrequency serializer."""

    account = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    month = serializers.DateField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("month"):
            data["date"] = str(data.pop("month"))[:7]
        return data
