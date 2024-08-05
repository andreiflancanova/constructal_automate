from cbeb.models.material import Material
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from cbeb.models import StiffenedPlateAnalysis
from cbeb.services import StiffenedPlateAnalysisService


class StiffenedPlateAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StiffenedPlateAnalysis
        fields = '__all__'

    def create(self, validated_data: StiffenedPlateAnalysis):
        stiffened_plate_id = validated_data.pop('stiffened_plate').id
        material_id = validated_data.pop('material').id
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=stiffened_plate_id)
        associated_material = get_object_or_404(Material, id=material_id)

        # Criar instância do StiffenedPlateAnalysis
        stiffened_plate_analysis_instance = StiffenedPlateAnalysis.objects.create(
            stiffened_plate=associated_stiffened_plate,
            material=associated_material,
            **validated_data
        )

        # Executar o serviço
        service = StiffenedPlateAnalysisService()
        service.create(
            stiffened_plate_analysis_instance,
            associated_stiffened_plate,
            associated_material
        )

        stiffened_plate_analysis_instance.refresh_from_db()
        
        return stiffened_plate_analysis_instance
