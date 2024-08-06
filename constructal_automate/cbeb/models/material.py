from django.db import models


class Material(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True)
    young_modulus = models.DecimalField(max_digits=8, decimal_places=2)
    poisson_ratio = models.DecimalField(max_digits=4, decimal_places=3)
    yielding_stress = models.DecimalField(max_digits=6, decimal_places=2)
    tang_modulus = models.DecimalField(max_digits=8, decimal_places=2)