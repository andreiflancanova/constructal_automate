from cbeb.models.biaxial_elastic_buckling import BiaxialElasticBuckling
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.services.biaxial_elastic_buckling_service import BiaxialElasticBucklingService
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404

class BiaxialElasticBucklingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiaxialElasticBuckling
        fields = '__all__'

    def create(self, validated_data: BiaxialElasticBuckling):
        stiffened_plate_analysis_id = validated_data.pop('stiffened_plate_analysis').id
        associated_stiffened_plate_analysis = get_object_or_404(StiffenedPlateAnalysis, id=stiffened_plate_analysis_id)
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=associated_stiffened_plate_analysis.stiffened_plate.id)
        
        n_x = validated_data['n_x']
        csi_y = validated_data['csi_y']
        
        service = BiaxialElasticBucklingService()
        
        n_cr, sigma_cr = service.create(
            associated_stiffened_plate_analysis,
            associated_stiffened_plate,
            n_x,
            csi_y
        )
        
        biaxial_elastic_buckling_instance = BiaxialElasticBuckling.objects.create(
            stiffened_plate_analysis=associated_stiffened_plate_analysis,
            n_cr=n_cr,
            sigma_cr=sigma_cr,
            **validated_data
        )

        return biaxial_elastic_buckling_instance