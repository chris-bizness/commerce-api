from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from validation.serializers import PaymentCardNumberSerializer


class ValidateCardView(APIView):
    def post(self, request):
        serializer = PaymentCardNumberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
