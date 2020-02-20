from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.helpers import AgentCursorPagination
from api.serializers import *
from common.models import District, Agent, HouseType


@api_view(('GET', ))
def get_provinces(request):
    """获取省级行政单位"""
    queryset = District.objects.filter(parent__isnull=True)\
        .only('name')
    serializer = DistrictSimpleSerializer(queryset, many=True)
    return Response({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer.data
    })


@api_view(('GET', ))
def get_district(request, distid):
    """获取地区详情"""
    district = District.objects.filter(distid=distid)\
        .defer('parent').first()
    serializer = DistrictDetailSerializer(district)
    return Response(serializer.data)


class AgentView(RetrieveUpdateAPIView, ListCreateAPIView):
    """经理人视图"""
    pagination_class = AgentCursorPagination

    def get_queryset(self):
        queryset = Agent.objects.all()
        if 'pk' not in self.kwargs:
            queryset = queryset.only('name', 'tel', 'servstar')
        else:
            queryset = queryset.prefetch_related(
                Prefetch('estates',
                         queryset=Estate.objects.all().only('name').order_by('-hot'))
            )
        return queryset.order_by('-servstar')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AgentCreateSerializer
        else:
            return AgentDetailSerializer if 'pk' in self.kwargs else AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)


class HouseTypeViewSet(ModelViewSet):
    """户型视图集"""
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None


class EstateViewSet(ReadOnlyModelViewSet):
    """楼盘视图集"""
    queryset = Estate.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.only('name')
        else:
            queryset = self.queryset\
                .defer('district__parent', 'district__ishot', 'district__intro')\
                .select_related('district')
        return queryset

    def get_serializer_class(self):
        return EstateDetailSerializer if self.action == 'retrieve' else EstateSimpleSerializer
