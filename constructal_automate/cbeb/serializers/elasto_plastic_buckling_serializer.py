from cbeb.models.elasto_plastic_buckling import ElastoPlasticBuckling
from cbeb.models.elastic_buckling import ElasticBuckling
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.services.elasto_plastic_buckling_service import ElastoPlasticBucklingService
from cbeb.strategies.biaxially_stiffened_plate_strategy import BiaxiallyStiffenedPlateStrategy
from cbeb.strategies.longitudinally_stiffened_plate_strategy import LongitudinallyStiffenedPlateStrategy
from cbeb.strategies.transversally_stiffened_plate_strategy import TransversallyStiffenedPlateStrategy
from cbeb.strategies.unstiffened_plate_strategy import UnstiffenedPlateStrategy
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ElastoPlasticBucklingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElastoPlasticBuckling
        fields = '__all__'

    def is_stiffened_plate(self, h_s, t_s):
        return h_s != 0.00 and t_s != 0.00
    
    def define_plate_strategy(self, associated_stiffened_plate):
        h_s = associated_stiffened_plate.h_s
        t_s = associated_stiffened_plate.t_s
        N_ls = associated_stiffened_plate.N_ls
        N_ts = associated_stiffened_plate.N_ts

        if self.is_stiffened_plate(h_s, t_s):
            if N_ls != 0.000 and N_ts != 0.000:
                return BiaxiallyStiffenedPlateStrategy()
            else:
                if N_ls == 0.000:
                    return TransversallyStiffenedPlateStrategy()
                else:
                    return LongitudinallyStiffenedPlateStrategy()
        else:
            return UnstiffenedPlateStrategy()

    def create(self, validated_data: ElastoPlasticBuckling):
        stiffened_plate_analysis_id = validated_data.pop('stiffened_plate_analysis').id
        associated_stiffened_plate_analysis = get_object_or_404(StiffenedPlateAnalysis, id=stiffened_plate_analysis_id)
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=associated_stiffened_plate_analysis.stiffened_plate.id)

        strategy = self.define_plate_strategy(associated_stiffened_plate)

        service = ElastoPlasticBucklingService(strategy)

        p_u_ts, p_u_ls, n_u, sigma_u_ts, sigma_u_ls, w_max, von_mises_dist_img_path, w_dist_img_path = service.create(
            associated_stiffened_plate,
            associated_stiffened_plate_analysis,
        )

        elasto_plastic_buckling_instance = ElastoPlasticBuckling.objects.create(
            stiffened_plate_analysis=associated_stiffened_plate_analysis,
            p_u_ts=p_u_ts,
            p_u_ls=p_u_ls,
            n_u=n_u,
            sigma_u_ts=sigma_u_ts,
            sigma_u_ls=sigma_u_ls,
            w_max=w_max,
            von_mises_dist_img_path=von_mises_dist_img_path,
            w_dist_img_path=w_dist_img_path
        )

        return elasto_plastic_buckling_instance