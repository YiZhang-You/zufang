import json

from django_redis import get_redis_connection
from rest_framework import serializers

from common.models import District, Agent, Estate, HouseType


class DistrictSimpleSerializer(serializers.ModelSerializer):
    """地区简单序列化器"""

    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):
    """地区详情序列化器"""
    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        redis_cli = get_redis_connection()
        data = redis_cli.get(f'zufang:district:{district.distid}:cities')
        if data:
            data = json.loads(data)
        if not data:
            queryset = District.objects.filter(parent=district).only('name')
            data = DistrictSimpleSerializer(queryset, many=True).data
            redis_cli.set(f'zufang:district:{district.distid}:cities', json.dumps(data), ex=900)
        return data

    class Meta:
        model = District
        exclude = ('parent', )


class AgentSimpleSerializer(serializers.ModelSerializer):
    """经理人简单序列化器"""

    class Meta:
        model = Agent
        fields = ('agentid', 'name', 'tel', 'servstar')


class AgentCreateSerializer(serializers.ModelSerializer):
    """创建经理人序列化器"""

    class Meta:
        model = Agent
        exclude = ('estates', )


class AgentDetailSerializer(serializers.ModelSerializer):
    """经理人详情序列化器"""
    estates = serializers.SerializerMethodField()

    @staticmethod
    def get_estates(agent):
        queryset = agent.estates.all()[:5]
        return EstateSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class EstateSimpleSerializer(serializers.ModelSerializer):
    """楼盘简单序列化器"""

    class Meta:
        model = Estate
        fields = ('estateid', 'name')


class EstateDetailSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()

    @staticmethod
    def get_district(estate):
        return DistrictSimpleSerializer(estate.district).data

    class Meta:
        model = Estate
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    """户型序列化器"""

    class Meta:
        model = HouseType
        fields = '__all__'
