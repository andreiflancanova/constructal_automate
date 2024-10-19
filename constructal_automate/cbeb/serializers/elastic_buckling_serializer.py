from cbeb.models.elastic_buckling import ElasticBuckling
from cbeb.models.stiffened_plate_analysis import StiffenedPlateAnalysis
from cbeb.services.elastic_buckling_service import ElasticBucklingService
from cbeb.strategies.biaxially_stiffened_plate_strategy import BiaxiallyStiffenedPlateStrategy
from cbeb.strategies.longitudinally_stiffened_plate_strategy import LongitudinallyStiffenedPlateStrategy
from cbeb.strategies.unstiffened_plate_strategy import UnstiffenedPlateStrategy
from cbeb.strategies.transversally_stiffened_plate_strategy import TransversallyStiffenedPlateStrategy
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ElasticBucklingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElasticBuckling
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

    def create(self, validated_data: ElasticBuckling):
        stiffened_plate_analysis_id = validated_data.pop('stiffened_plate_analysis').id
        associated_stiffened_plate_analysis = get_object_or_404(StiffenedPlateAnalysis, id=stiffened_plate_analysis_id)
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=associated_stiffened_plate_analysis.stiffened_plate.id)


        strategy = self.define_plate_strategy(associated_stiffened_plate)

        service = ElasticBucklingService(strategy)

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