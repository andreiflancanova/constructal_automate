from django.db import models
from .plate import Plate


class StiffenedPlate(models.Model):
    id = models.BigAutoField(primary_key=True)
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE)
    phi = models.DecimalField(max_digits=5, decimal_places=4)
    N_ls = models.IntegerField()
    N_ts = models.IntegerField()
    k = models.DecimalField(max_digits=6, decimal_places=3)
    t_1 = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    h_s = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    t_s = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    length_ts = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    length_ls = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    area_ts = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    area_ls = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    t_eq_ts = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    t_eq_ls = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(null=True)