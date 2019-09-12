from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from card_api.serializers import PaymentCardNumberSerializer
from common.algorithms import (
    generate_card_number,
    generate_card_number_from_issuer
)
from card_api.schemas import (
    ValidateCardSchema,
    GenerateCardSchema,
)
from common.constants import (
    MIN_PAYMENT_CARD_NUMBER_LENGTH as MIN_LENGTH,
    MAX_PAYMENT_CARD_NUMBER_LENGTH as MAX_LENGTH,
)


def _get_payment_card_number_response(**kwargs):
    serializer = PaymentCardNumberSerializer(data=kwargs)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateCardView(APIView):
    schema = ValidateCardSchema()

    def post(self, request):
        return _get_payment_card_number_response(**request.data)


class GenerateCardView(APIView):
    schema = GenerateCardSchema()

    def _bad(self, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, list):
                kwargs[k] = [v]
        return Response(kwargs, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        num_digits = request.query_params.get('length')
        issuer = request.query_params.get('issuer')
        prefix = request.query_params.get('prefix')

        if issuer and (prefix or num_digits is not None):
            return self._bad(
                issuer="cannot be specified with `prefix` or `length`"
            )
        if issuer:
            try:
                number = generate_card_number_from_issuer(issuer)
            except Exception as e:
                return self._bad(issuer=str(e))
        else:
            inputs = {}
            if num_digits is not None:
                if num_digits < MIN_LENGTH or num_digits > MAX_LENGTH:
                    return self._bad(
                        length="Must be between [{MIN_LENGTH}, {MAX_LENGTH}],"
                        " inclusive."
                    )
                inputs['num_digits'] = int(num_digits)
            if prefix:
                inputs['prefix'] = prefix
            try:
                number = generate_card_number(**inputs)
            except Exception as e:
                return self._bad(prefix=str(e))
        return _get_payment_card_number_response(number=number, private=False)
