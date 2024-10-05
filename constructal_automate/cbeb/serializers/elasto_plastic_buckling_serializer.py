from cbeb.models.elasto_plastic_buckling import ElastoPlasticBuckling
from cbeb.models.elastic_buckling import ElasticBuckling
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.services.elasto_plastic_buckling_service import ElastoPlasticBucklingService
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ElastoPlasticBucklingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElastoPlasticBuckling
        fields = '__all__'

    def create(self, validated_data: ElastoPlasticBuckling):
        stiffened_plate_analysis_id = validated_data.pop('stiffened_plate_analysis').id
        associated_stiffened_plate_analysis = get_object_or_404(StiffenedPlateAnalysis, id=stiffened_plate_analysis_id)
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=associated_stiffened_plate_analysis.stiffened_plate.id)
        associated_elastic_buckling = get_object_or_404(ElasticBuckling, stiffened_plate_analysis_id=associated_stiffened_plate_analysis.id)

        service = ElastoPlasticBucklingService()

        n_u, sigma_u, w_max, von_mises_dist_img_path, w_dist_img_path = service.create(
            associated_stiffened_plate,
            associated_stiffened_plate_analysis,
            associated_elastic_buckling
        )

        # TODO: Implementar lógica para gerar as imagens
        elasto_plastic_buckling_instance = ElastoPlasticBuckling.objects.create(
            stiffened_plate_analysis=associated_stiffened_plate_analysis,
            n_u=n_u,
            sigma_u=sigma_u,
            w_max=w_max,
            von_mises_dist_img_path=von_mises_dist_img_path,
            w_dist_img_path=w_dist_img_path
        )

        return elasto_plastic_buckling_instance