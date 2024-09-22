from django.db import models

from cbeb.models.processing_status import ProcessingStatus
from .buckling_load_type import BucklingLoadType
from csg.models.stiffened_plate import StiffenedPlate
from .material import Material


class StiffenedPlateAnalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stiffened_plate = models.ForeignKey(StiffenedPlate, on_delete=models.CASCADE)
    buckling_load_type = models.ForeignKey(BucklingLoadType, on_delete=models.CASCADE)
    mesh_size = models.DecimalField(max_digits=4, decimal_places=1)
    num_elem = models.PositiveIntegerField(null=True)
    case_study = models.TextField(null=True)
    analysis_dir_path = models.TextField(null=True)
    analysis_rst_file_path = models.TextField(null=True)
    analysis_lgw_file_path = models.TextField(null=True)
    elastic_buckling_status = models.ForeignKey(ProcessingStatus, on_delete=models.CASCADE, null=True, blank=True, related_name='elastic_buckling_stiffenedplateanalysis_set')
    elasto_plastic_buckling_status = models.ForeignKey(ProcessingStatus, on_delete=models.CASCADE, null=True, blank=True, related_name='elastoplastic_buckling_stiffenedplateanalysis_set')