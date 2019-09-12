from django.urls import path
from card_api.views import (
    ValidateCardView,
    GenerateCardFromIssuerView,
    GenerateCardFromPrefixView
)

urlpatterns = [
    path('validate/', ValidateCardView.as_view()),
    path('generate/<str:issuer>', GenerateCardFromIssuerView.as_view()),
    path('generate/from/<str:prefix>', GenerateCardFromPrefixView.as_view()),
]
