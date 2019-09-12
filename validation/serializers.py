from rest_framework import serializers
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)
from common.objects import PaymentCardNumber


class PaymentCardNumberSerializer(serializers.Serializer):
    number = serializers.CharField(min_length=MIN_LENGTH, max_length=MAX_LENGTH)

    def create(self, validated_data):
        return PaymentCardNumber(validated_data['number'])

    def to_representation(self, instance):
        return {
            'isValid': instance.is_valid,

            'majorIndustryIdentifier': instance.mii,
            'issuerIdentificationNumber': instance.iin,
            'personalAccountNumber': instance.account_number,
            'checkDigit': instance.check_digit,
        }
