from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class Resident(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    items = models.ManyToManyField('Item', blank=True)
    date_of_admittance = models.DateField(default=datetime.now)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

   
class Item(models.Model):
    name = models.CharField(max_length=255)

class Comment(models.Model):
    resident = models.ForeignKey(Resident, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    pass