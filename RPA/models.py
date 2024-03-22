from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class lm_tbl(models.Model):
    PartName = models.IntegerField()

class part_tbl(models.Model):
    PartName = models.IntegerField()

class running_part_tbl(models.Model):
    Part_Name = models.CharField(max_length=255, null=True, default="")
    prod_status = models.IntegerField(default=0)

