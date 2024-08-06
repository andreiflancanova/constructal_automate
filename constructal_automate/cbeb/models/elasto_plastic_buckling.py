from django.db import models

from .elastic_buckling import ElasticBuckling

from .stiffened_plate_analysis import StiffenedPlateAnalysis


class ElastoPlasticBuckling(models.Model):
    id = models.BigAutoField(primary_key=True)
    stiffened_plate_analysis = models.ForeignKey(StiffenedPlateAnalysis, on_delete=models.CASCADE)
    elastic_buckling = models.ForeignKey(ElasticBuckling)
    n_yield = models.DecimalField(max_digits=7, decimal_places=3)
    n_u = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    sigma_u = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    w_max = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    w_dist_img_path = models.TextField(null=True)
    von_mises_dist_img_path = models.TextField(null=True)