from django.db import models

# Create your models here.
class Doctor(models.Model):
    """Doctor that is generated"""
    date_added = models.DateTimeField(auto_now_add=True)


