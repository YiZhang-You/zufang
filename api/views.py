import re

from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response

from api.serializers import *
from common.models import District, Agent


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
def get_district(request: HttpRequest, distid) -> HttpResponse:
    district = District.objects.filter(distid=distid)\
        .defer('parent').first()
    serializer = DistrictDetailSerializer(district)
    return Response(serializer.data)


class AgentView(RetrieveUpdateAPIView, ListCreateAPIView):

    def get_queryset(self):
        queryset = Agent.objects.all()
        if 'pk' not in self.kwargs:
            queryset = queryset.only('name', 'tel', 'servstar')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AgentCreateSerializer
        else:
            return AgentDetailSerializer if 'pk' in self.kwargs else AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)
