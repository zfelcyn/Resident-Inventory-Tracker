from django.contrib import admin
from .models import Resident, Item, CustomUser

# Register your models here.

admin.site.register(Resident)
admin.site.register(Item)
admin.site.register(CustomUser)