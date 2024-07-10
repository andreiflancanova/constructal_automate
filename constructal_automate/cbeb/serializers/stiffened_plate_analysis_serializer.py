from rest_framework import serializers
from django.shortcuts import get_object_or_404

from cbeb.models import StiffenedPlateAnalysis
from cbeb.services import StiffenedPlateAnalysisService

class StiffenedPlateAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StiffenedPlateAnalysis
        fields = '__all__'
        
    def retrieve(self):
        service = StiffenedPlateAnalysisService()
        return service.validate_mapdl_connection()