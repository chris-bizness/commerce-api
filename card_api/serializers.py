from rest_framework import serializers
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)
from common.objects import PaymentCardNumber
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
    private = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return PaymentCardNumber(validated_data['number'])

    def to_representation(self, instance):
        retval = {
            'isValid': instance.is_valid,

            'majorIndustryIdentifier': instance.mii,
            'issuerIdentificationNumber': instance.iin,
            'personalAccountNumber': instance.account_number,
            'checkDigit': instance.check_digit,
        }
        if instance.is_valid and instance.issuer:
            retval['issuer'] = instance.issuer
        if not self.validated_data.get('private'):
            retval = {
                "number": instance.value,
                "details": retval
            }
        return retval
