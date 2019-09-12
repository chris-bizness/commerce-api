from django.urls import path
from card_api.views import ValidateCardView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('validate/', ValidateCardView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
