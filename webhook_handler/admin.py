from django.contrib import admin

# Register your models here.
from .models import Machine,SensorData, LatestSensorData,Task,MaintenanceProfile


admin.site.register(Machine)
admin.site.register(SensorData)
admin.site.register(LatestSensorData)
admin.site.register(Task)
admin.site.register(MaintenanceProfile)