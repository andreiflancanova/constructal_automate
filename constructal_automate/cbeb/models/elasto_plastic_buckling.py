from django.db import models
from .stiffened_plate_analysis import StiffenedPlateAnalysis


class ElastoPlasticBuckling(models.Model):
    id = models.BigAutoField(primary_key=True)
    stiffened_plate_analysis = models.ForeignKey(StiffenedPlateAnalysis, on_delete=models.CASCADE)
    p_u = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    n_u = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    sigma_u = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    w_max = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    w_dist_img_path = models.TextField(null=True)
    von_mises_dist_img_path = models.TextField(null=True)