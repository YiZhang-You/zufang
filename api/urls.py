from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import get_provinces, get_district, HotCityView, \
    AgentViewSet, HouseTypeViewSet, EstateViewSet, TagViewSet, \
    HouseInfoViewSet, get_code_by_sms, login, UserViewSet, \
    upload_house_photo, logout

urlpatterns = [
    path('photos/', upload_house_photo),
    path('token/', login),
    path('token/<str:token>', logout),
    path('mobile/<str:tel>/', get_code_by_sms),
    path('districts/', get_provinces),
    path('districts/<int:distid>/', get_district),
    path('hotcities/', HotCityView.as_view()),
]

router = SimpleRouter()
router.register('housetypes', HouseTypeViewSet)
router.register('estates', EstateViewSet)
router.register('agents', AgentViewSet)
router.register('tags', TagViewSet)
router.register('houseinfos', HouseInfoViewSet)
router.register('users', UserViewSet)
urlpatterns += router.urls
