from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import DistrictSimpleSerializer, DistrictDetailSerializer
from common.models import District


@api_view(('GET', ))
def get_provinces(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)\
        .only('name')
    serializer = DistrictSimpleSerializer(queryset, many=True)
    return Response({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer.data
    })


@api_view(('GET', ))
def get_cities(request: HttpRequest, distid) -> HttpResponse:
    district = District.objects.filter(distid=distid)\
        .defer('parent').first()
    serializer = DistrictDetailSerializer(district)
    return Response(serializer.data)


