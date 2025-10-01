from django.db import models

# Create your models here.
class Doctor(models.Model):
    """Doctor that is generated"""
    date_added = models.DateTimeField(auto_now_add=True)

class DoctorChat(models.Model):
    """Chat about the Doctor"""
    my_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class HomeChat(models.Model):
    """Chat that will generate a Doctor"""
