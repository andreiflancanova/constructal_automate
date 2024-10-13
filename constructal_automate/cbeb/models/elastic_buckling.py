from django.db import models
from .stiffened_plate_analysis import StiffenedPlateAnalysis


class ElasticBuckling(models.Model):
    id = models.BigAutoField(primary_key=True)
    stiffened_plate_analysis = models.ForeignKey(StiffenedPlateAnalysis, on_delete=models.CASCADE)
    n_cr = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    sigma_cr_ts = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    sigma_cr_ls = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    w_center = models.DecimalField(max_digits=8, decimal_places=4, null=True)
