from django.contrib import admin

# Register your models here.
from .models import machines,machine_type,machine_data


admin.site.register(machine_data)
admin.site.register(machine_type)
admin.site.register(machines)
