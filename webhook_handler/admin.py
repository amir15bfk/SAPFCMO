from django.contrib import admin

# Register your models here.
from .models import Machine,SensorData, LatestSensorData


admin.site.register(Machine)
admin.site.register(SensorData)
admin.site.register(LatestSensorData)