from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class parkuser(AbstractUser):
    Choices_Role = [("ADMIN", "ADMIN"), ("PUBLIC", "PUBLIC")]
    role = models.CharField(max_length=20, choices=Choices_Role, default='PUBLIC')

class parkspace(models.Model):
    Level = models.IntegerField()
    TWA = models.IntegerField()
    FWA = models.IntegerField()
    
class parkhistory(models.Model):
    Choices_Type = [("TWA", "TWA"), ("FWA", "FWA")]
    Level = models.IntegerField()
    Type = models.CharField(max_length=5, choices=Choices_Type, default='FWA')
    VehicleNumber = models.CharField(max_length=10)
    Lot = models.IntegerField()
    Intime = models.DateTimeField(null=True,blank=True)
    Outtime = models.DateTimeField(null=True,blank=True)
    Fee = models.IntegerField(null=True,blank=True)