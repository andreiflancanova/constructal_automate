from django.db import models

LONGITUDINAL_GEOMETRY_MAX_DIGITS=8
LONGITUDINAL_GEOMETRY_DECIMAL_PLACES=2

class Plate(models.Model):
    id = models.BigAutoField(primary_key=True)
    a = models.DecimalField(max_digits=LONGITUDINAL_GEOMETRY_MAX_DIGITS, decimal_places=LONGITUDINAL_GEOMETRY_DECIMAL_PLACES)
    b = models.DecimalField(max_digits=LONGITUDINAL_GEOMETRY_MAX_DIGITS, decimal_places=LONGITUDINAL_GEOMETRY_DECIMAL_PLACES)
    t_0 = models.DecimalField(max_digits=LONGITUDINAL_GEOMETRY_MAX_DIGITS, decimal_places=LONGITUDINAL_GEOMETRY_DECIMAL_PLACES)