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
    GenerateCardFromIssuerSchema,
    GenerateCardFromPrefixSchema,
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


class GenerateCardFromIssuerView(APIView):
    schema = GenerateCardFromIssuerSchema()

    def get(self, request, issuer):
        try:
            number = generate_card_number_from_issuer(issuer)
        except Exception as e:
            return Response(
                {'issuer': [str(e)]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return _get_payment_card_number_response(number=number, private=False)


class GenerateCardFromPrefixView(APIView):
    schema = GenerateCardFromPrefixSchema()

    def get(self, request, prefix):
        try:
            number = generate_card_number(prefix)
        except Exception as e:
            return Response(
                {'issuer': [str(e)]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return _get_payment_card_number_response(number=number, private=False)
