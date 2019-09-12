from django.urls import path, include

urlpatterns = [
    path('', include('card_api.urls')),
]
