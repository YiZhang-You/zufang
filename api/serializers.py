from rest_framework import serializers

from common.models import District, Agent, Estate


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
        queryset = District.objects.filter(parent=district).only('name')
        return DistrictSimpleSerializer(queryset, many=True).data

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
        queryset = agent.estates.all().only('name')
        return EstateSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class EstateSimpleSerializer(serializers.ModelSerializer):
    """楼盘简单序列化器"""

    class Meta:
        model = Estate
        fields = ('estateid', 'name')
