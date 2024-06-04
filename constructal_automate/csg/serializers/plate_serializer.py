from rest_framework import serializers
from csg.models import Plate


class PlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plate
        fields = '__all__'
