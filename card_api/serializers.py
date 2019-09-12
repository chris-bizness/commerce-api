from rest_framework import serializers
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)
from common.objects import PaymentCardNumber
from typing import Dict, Any
from card_api.validators import (
    validate_contains_only_digits_and_separators,
    LengthWithoutSeparatorsValidator
)


class PaymentCardNumberSerializer(serializers.Serializer):
    number = serializers.CharField(
        validators=[
            validate_contains_only_digits_and_separators,
            LengthWithoutSeparatorsValidator(min=MIN_LENGTH, max=MAX_LENGTH)
        ]
    )

    def create(self, validated_data: Dict[str, Any]) -> PaymentCardNumber:
        return PaymentCardNumber(validated_data['number'])

    def to_representation(self, instance: PaymentCardNumber) -> Dict[str, Any]:
        retval = {
            'isValid': instance.is_valid,

            'majorIndustryIdentifier': instance.mii,
            'issuerIdentificationNumber': instance.iin,
            'personalAccountNumber': instance.account_number,
            'checkDigit': instance.check_digit,
        }
        if instance.is_valid and instance.issuer:
            retval['issuer'] = instance.issuer
        return retval
