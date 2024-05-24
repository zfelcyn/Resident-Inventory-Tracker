from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    items = models.ManyToManyField('Item', blank=True)

class Item(models.Model):
    name = models.CharField(max_length=255)


class CustomUser(AbstractUser):
    pass