from django.db import models

# Create your models here.
class machines(models.Model):
    name=models.CharField(max_length=100)
    machine_type=models.ForeignKey('machine_type',on_delete=models.CASCADE)


class machine_type(models.Model):
    name=models.CharField(max_length=100)
    
class machine_data(models.Model):
    machine=models.ForeignKey('machines',on_delete=models.CASCADE)
    #data is a float
    data=models.FloatField()
    timestamp=models.DateTimeField()
    #statues binarie
    status=models.BooleanField(default=False)