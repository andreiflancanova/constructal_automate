from django.db import models

from .stiffened_plate_analysis import StiffenedPlateAnalysis


class BiaxialElasticBuckling(models.Model):
    id = models.BigAutoField(primary_key=True)
    stiffened_plate_analysis = models.ForeignKey(StiffenedPlateAnalysis, on_delete=models.CASCADE)
    n_x = models.DecimalField(max_digits=7, decimal_places=3) 
    csi_y = models.DecimalField(max_digits=4, decimal_places=3) 
    n_cr = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    sigma_cr = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    w_max = models.DecimalField(max_digits=8, decimal_places=4, null=True)
