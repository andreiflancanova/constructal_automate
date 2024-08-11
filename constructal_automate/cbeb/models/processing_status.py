from django.db import models

class ProcessingStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=True)