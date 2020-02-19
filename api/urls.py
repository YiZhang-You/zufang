from django.urls import path

from api.views import get_provinces, get_district, AgentView

urlpatterns = [
    path('districts/', get_provinces),
    path('districts/<int:distid>/', get_district),
    path('agents/', AgentView.as_view()),
    path('agents/<int:pk>/', AgentView.as_view()),
]
