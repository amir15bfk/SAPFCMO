# # Create your models here.
# # webhook_handler/models.py
# from django.db import models

# class MachineData(models.Model):
#     machine_id = models.CharField(max_length=50)
#     timestamp = models.DateTimeField()
#     weld_temperature = models.FloatField()
#     weld_current = models.FloatField()
#     weld_voltage = models.FloatField()
#     weld_time = models.IntegerField()
#     pressure_applied = models.FloatField()
#     arm_position_x = models.FloatField()
#     arm_position_y = models.FloatField()
#     arm_position_z = models.FloatField()
#     wire_feed_rate = models.FloatField()
#     gas_flow_rate = models.FloatField()
#     weld_strength_estimate = models.FloatField()
#     vibration_level = models.FloatField()
#     power_consumption = models.FloatField()

#     def __str__(self):
#         return f'{self.machine_id} - {self.timestamp}'
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Machine(models.Model):
    MACHINE_TYPES = (
        ('WELDING', 'Welding Robot'),
        ('STAMPING', 'Stamping Press'),
        ('PAINTING', 'Painting Robot'),
        ('AGV', 'AGV'),
        ('CNC', 'CNC Machine'),
        ('LEAK_TEST', 'Leak Test Machine'),
    )

    machine_id = models.CharField(max_length=50, unique=True)
    machine_type = models.CharField(max_length=20, choices=MACHINE_TYPES)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    webhook_url = models.URLField()
    @property
    def latest_data(self):
        return self.sensor_data.order_by('-timestamp').first()
    @property
    def latest_20_data(self):
        return self.sensor_data.order_by('-timestamp')[:20]
    @property
    def all_data(self):
        return self.sensor_data.order_by('timestamp')
    
    def __str__(self):
        return f"{self.machine_type} - {self.machine_id}"

class SensorData(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='sensor_data')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    data = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['machine', '-timestamp']),
        ]

    def __str__(self):
        return f"Data for {self.machine} at {self.timestamp}"

class LatestSensorData(models.Model):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, related_name='latest_data')
    timestamp = models.DateTimeField(auto_now=True)
    data = models.JSONField()

    def __str__(self):
        return f"Latest data for {self.machine}"
    

class MaintenanceAgent(models.Model):
    # Define the possible states for the agent
    AGENT_STATES = [
        ('working', 'Working'),
        ('free', 'Free'),
        ('not_at_work', 'Not at Work'),
    ]

    # Fields for the MaintenanceAgent
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Agent's name
    state = models.CharField(max_length=12, choices=AGENT_STATES, default='free')  # State of the agent
    assigned_tasks = models.ManyToManyField('Task', related_name='agents', blank=True)  # List of tasks assigned

    # Optional fields (e.g., shift, contact, etc.)
    contact = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    # Fields for Task
    title = models.CharField(max_length=200)  # Task title or description
    description = models.TextField(blank=True, null=True)  # Detailed description of the task
    start_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    completed = models.BooleanField(default=False)  # Whether the task is completed or not

    # Reference to the Machine model
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE, related_name='tasks')  # Task related to a specific machine

    def __str__(self):
        return self.title
