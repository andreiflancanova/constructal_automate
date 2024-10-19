from cbeb.models.material import Material
from cbeb.strategies.unstiffened_plate_strategy import UnstiffenedPlateStrategy
from cbeb.strategies.biaxially_stiffened_plate_strategy import BiaxiallyStiffenedPlateStrategy
from cbeb.strategies.longitudinally_stiffened_plate_strategy import LongitudinallyStiffenedPlateStrategy
from cbeb.strategies.transversally_stiffened_plate_strategy import TransversallyStiffenedPlateStrategy
from csg.models.stiffened_plate import StiffenedPlate
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from cbeb.models import StiffenedPlateAnalysis
from cbeb.services import StiffenedPlateAnalysisService
import logging

log = logging.getLogger(__name__)

class StiffenedPlateAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StiffenedPlateAnalysis
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
                log.info('Entering BiaxiallyStiffenedPlateStrategy in StiffenedPlateAnalysisSerializer...')
                return BiaxiallyStiffenedPlateStrategy()
            else:
                if N_ls == 0.000:
                    log.info('Entering TransversallyStiffenedPlateStrategy in StiffenedPlateAnalysisSerializer...')
                    return TransversallyStiffenedPlateStrategy()
                if N_ts == 0.000:
                    log.info('Entering LongitudinallyStiffenedPlateStrategy in StiffenedPlateAnalysisSerializer...')
                    return LongitudinallyStiffenedPlateStrategy()
        else:
            log.info('Entering UnstiffenedPlateStrategy in StiffenedPlateAnalysisSerializer...')
            return UnstiffenedPlateStrategy()

    def create(self, validated_data: StiffenedPlateAnalysis):
        stiffened_plate_id = validated_data.pop('stiffened_plate').id
        material_id = validated_data.pop('material').id
        associated_stiffened_plate = get_object_or_404(StiffenedPlate, id=stiffened_plate_id)
        associated_material = get_object_or_404(Material, id=material_id)

        # Criar instância do StiffenedPlateAnalysisSerializer
        stiffened_plate_analysis_instance = StiffenedPlateAnalysis.objects.create(
            stiffened_plate=associated_stiffened_plate,
            material=associated_material,
            **validated_data
        )

        strategy = self.define_plate_strategy(associated_stiffened_plate)

        # Executar o serviço
        service = StiffenedPlateAnalysisService(strategy)
        service.create(
            stiffened_plate_analysis_instance,
            associated_stiffened_plate,
            associated_material
        )

        stiffened_plate_analysis_instance.refresh_from_db()
        
        return stiffened_plate_analysis_instance
