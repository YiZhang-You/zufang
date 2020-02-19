from django.urls import path

from api.views import get_provinces, get_cities

urlpatterns = [
    path('districts/', get_provinces),
    path('districts/<int:distid>/', get_cities),
]
