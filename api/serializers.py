from rest_framework import serializers

from common.models import District


class DistrictSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        queryset = District.objects.filter(parent=district).only('name')
        return DistrictSimpleSerializer(queryset, many=True).data

    class Meta:
        model = District
        exclude = ('parent', )
