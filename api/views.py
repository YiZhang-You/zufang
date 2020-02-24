from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.helpers import EstateFilterSet, HouseInfoFilterSet
from api.serializers import *
from common.models import District, Agent, HouseType, Tag


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
#         caches['default'].set(f'district:{distid}', district, timeout=900)
#     serializer = DistrictDetailSerializer(district)
#     return Response(serializer.data)


@api_view(('GET', ))
def get_district(request, distid):
    """获取地区详情"""
    redis_cli = get_redis_connection()
    data = redis_cli.get(f'zufang:district:{distid}')
    if data:
        data = json.loads(data)
    else:
        district = District.objects.filter(distid=distid)\
            .defer('parent').first()
        data = DistrictDetailSerializer(district).data
        redis_cli.set(f'zufang:district:{distid}', json.dumps(data), ex=900)
    return Response(data)


@method_decorator(decorator=cache_page(timeout=86400), name='get')
class HotCityView(ListAPIView):
    """热门城市视图"""
    queryset = District.objects.filter(ishot=True).only('name')
    serializer_class = DistrictSimpleSerializer
    pagination_class = None


@method_decorator(decorator=cache_page(timeout=120), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class AgentViewSet(ModelViewSet):
    """经理人视图"""
    queryset = Agent.objects.all()

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            self.queryset = self.queryset.filter(name__startswith=name)
        servstar = self.request.GET.get('servstar')
        if servstar:
            self.queryset = self.queryset.filter(servstar__gte=servstar)
        if self.action == 'list':
            self.queryset = self.queryset.only('name', 'tel', 'servstar')
        else:
            self.queryset = self.queryset.prefetch_related(
                Prefetch('estates',
                         queryset=Estate.objects.all().only('name').order_by('-hot'))
            )
        return self.queryset.order_by('-servstar')

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return AgentCreateSerializer
        return AgentDetailSerializer if self.action == 'retrieve' \
            else AgentSimpleSerializer


@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
class HouseTypeViewSet(ModelViewSet):
    """户型视图集"""
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None


@method_decorator(decorator=cache_page(timeout=3600), name='list')
class TagViewSet(ModelViewSet):
    """房源标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@method_decorator(decorator=cache_page(timeout=300), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class EstateViewSet(ModelViewSet):
    """楼盘视图集"""
    queryset = Estate.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = EstateFilterSet
    ordering = '-hot'
    ordering_fields = ('district', 'hot', 'name')

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.only('name')
        else:
            queryset = self.queryset\
                .defer('district__parent', 'district__ishot', 'district__intro')\
                .select_related('district')
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return EstateCreateSerializer
        return EstateDetailSerializer if self.action == 'retrieve' \
            else EstateSimpleSerializer


@method_decorator(decorator=cache_page(timeout=120), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class HouseInfoViewSet(ModelViewSet):
    """房源视图集"""
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoDetailSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = HouseInfoFilterSet
    ordering = ('-pubdate', )
    ordering_fields = ('pubdate', 'price')

    @action(methods=('GET', ), detail=True)
    def photos(self, request, pk):
        queryset = HousePhoto.objects.filter(house=self.get_object())
        return Response(HousePhotoSerializer(queryset, many=True).data)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset\
                .only('houseid', 'title', 'area', 'floor', 'totalfloor', 'price',
                      'mainphoto', 'priceunit', 'street', 'type',
                      'district_level3__distid', 'district_level3__name')\
                .select_related('district_level3', 'type')\
                .prefetch_related('tags')
        return self.queryset\
            .defer('user', 'district_level2',
                   'district_level3__parent', 'district_level3__ishot', 'district_level3__intro',
                   'estate__district', 'estate__hot', 'estate__intro',
                   'agent__realstar', 'agent__profstar', 'agent__certificated')\
            .select_related('district_level3', 'type', 'estate', 'agent')\
            .prefetch_related('tags')

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return HouseInfoCreateSerializer
        return HouseInfoDetailSerializer if self.action == 'retrieve' \
            else HouseInfoSimpleSerializer
