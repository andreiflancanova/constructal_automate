from cbeb.models.elastic_buckling import ElasticBuckling
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.services.elastic_buckling_service import ElasticBucklingService
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ElasticBucklingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElasticBuckling
        fields = '__all__'

    def create(self, validated_data: ElasticBuckling):
        stiffened_plate_analysis_id = validated_data.pop('stiffened_plate_analysis').id
        associated_stiffened_plate_analysis = get_object_or_404(StiffenedPlateAnalysis, id=stiffened_plate_analysis_id)
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=associated_stiffened_plate_analysis.stiffened_plate.id)

        service = ElasticBucklingService()

        n_cr, sigma_cr_ts, sigma_cr_ls, w_center = service.create(
            associated_stiffened_plate_analysis,
            associated_stiffened_plate
        )

        elastic_buckling_instance = ElasticBuckling.objects.create(
            stiffened_plate_analysis=associated_stiffened_plate_analysis,
            n_cr=n_cr,
            sigma_cr_ts=sigma_cr_ts,
            sigma_cr_ls=sigma_cr_ls,
            w_center=w_center,
            **validated_data
        )

        return elastic_buckling_instance