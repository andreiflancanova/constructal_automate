from django.db import models

class BucklingLoadType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True)