from django.db import models

from constructal_automate.csg.models.stiffened_plate import StiffenedPlate
from .material import Material


class StiffenedPlateAnalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    stiffened_plate_id = models.ForeignKey(StiffenedPlate, on_delete=models.CASCADE)
    mesh_size = models.DecimalField(max_digits=4, decimal_places=1)
    description = models.TextField(null=True)
    results_dir_path = models.TextField(null=True)
    rst_file_path = models.TextField(null=True)
    lgw_file_path = models.TextField(null=True)