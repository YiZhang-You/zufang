import pickle

from django.core.cache import caches
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.helpers import AgentCursorPagination
from api.serializers import *
from common.models import District, Agent, HouseType


@cache_page(timeout=365 * 86400)
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


# @api_view(('GET', ))
# def get_district(request, distid):
#     """获取地区详情"""
#     district = caches['default'].get(f'district:{distid}')
#     if district is None:
#         district = District.objects.filter(distid=distid).first()
#         caches['default'].set(f'district:{distid}', district, ex=900)
#     serializer = DistrictDetailSerializer(district)
#     return Response(serializer.data)


@api_view(('GET', ))
def get_district(request, distid):
    """获取地区详情"""
    redis_cli = get_redis_connection()
    data = redis_cli.get(f'zufang:district:{distid}')
    if data:
        district = pickle.loads(data)
    else:
        district = District.objects.filter(distid=distid)\
            .defer('parent').first()
        data = pickle.dumps(district)
        redis_cli.set(f'zufang:district:{distid}', data, ex=900)
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


@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
class HouseTypeViewSet(ModelViewSet):
    """户型视图集"""
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None


@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
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
