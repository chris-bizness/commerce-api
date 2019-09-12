from django.urls import path
from card_api.views import (
    ValidateCardView,
    GenerateCardView,
)

urlpatterns = [
    path('validate', ValidateCardView.as_view()),
    path('generate', GenerateCardView.as_view()),
]
