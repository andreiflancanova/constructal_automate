from django.db import models
from plate import Plate

class StiffenedPlate(models.Model):
    id = models.BigAutoField(primary_key=True)
    plate_id = models.OneToOneField(
        Plate,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    phi = models.DecimalField(max_digits=5, decimal_places=4)
    N_ls = models.IntegerField()
    N_ts = models.IntegerField()
    k = models.DecimalField(max_digits=6, decimal_places=3)
    t_1 = models.DecimalField(max_digits=6, decimal_places=2)
    h_s = models.DecimalField(max_digits=6, decimal_places=2)
    t_s = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True)