from django.db import models

from csg.models.stiffened_plate import StiffenedPlate
from .material import Material


class StiffenedPlateAnalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    stiffened_plate = models.ForeignKey(StiffenedPlate, on_delete=models.CASCADE)
    mesh_size = models.DecimalField(max_digits=4, decimal_places=1)
    case_study = models.TextField(null=True)
    analysis_dir_path = models.TextField(null=True)
    analysis_rst_file_path = models.TextField(null=True)
    analysis_lgw_file_path = models.TextField(null=True)