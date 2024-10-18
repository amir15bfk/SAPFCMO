# Create your models here.
# webhook_handler/models.py
from django.db import models

class MachineData(models.Model):
    machine_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    weld_temperature = models.FloatField()
    weld_current = models.FloatField()
    weld_voltage = models.FloatField()
    weld_time = models.IntegerField()
    pressure_applied = models.FloatField()
    arm_position_x = models.FloatField()
    arm_position_y = models.FloatField()
    arm_position_z = models.FloatField()
    wire_feed_rate = models.FloatField()
    gas_flow_rate = models.FloatField()
    weld_strength_estimate = models.FloatField()
    vibration_level = models.FloatField()
    power_consumption = models.FloatField()

    def __str__(self):
        return f'{self.machine_id} - {self.timestamp}'
