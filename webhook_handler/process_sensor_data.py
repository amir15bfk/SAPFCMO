import os
import django
import pandas as pd
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SAPFCMO.settings')
django.setup()

from webhook_handler.models import SensorData
from webhook_handler.models import Machine

# Retrieve all machine data
machine_list = Machine.objects.all()

# Create a list of dictionaries to hold the machine data
#machine_data = []
#for machine in machine_list:
#    machine_data.append({
#        'ID': machine.machine_id,
#        'Name': machine.name,
#        'Type': machine.machine_type,
#
#    })
#    
#machine_df = pd.DataFrame(machine_data)



######################################################




# Retrieve all sensor data
sensor_data_list = SensorData.objects.all()
sensor_data = []

for sensor in sensor_data_list:

    sensor_json = sensor.data  # sensor.data is already a dictionary
    flattened_data = {
        'Machine': sensor.machine,
        'Type': sensor.machine.machine_type,
        'Machine ID': sensor.machine.machine_id,
        'Timestamp': sensor.timestamp,
        **sensor_json
    }
    sensor_data.append(flattened_data)

df_sensor = pd.DataFrame(sensor_data)
type_groups = df_sensor.groupby('Type')



# Save each group to a separate CSV file
for type_value, group in type_groups:
    
    group.dropna(axis=1, how='all', inplace=True)
    
    if 'arm_position' in group.columns:
        group['x'] = group['arm_position'].apply(lambda x: x.get('x'))
        group['y'] = group['arm_position'].apply(lambda x: x.get('y'))
        group['z'] = group['arm_position'].apply(lambda x: x.get('z'))
        group.drop(columns=['arm_position'], inplace=True)
        
    if 'location' in group.columns:
        group['x'] = group['location'].apply(lambda x: x.get('x'))
        group['y'] = group['location'].apply(lambda x: x.get('y'))
        group['z'] = group['location'].apply(lambda x: x.get('z'))        
        group.drop(columns=['location'], inplace=True)
        

    group.to_csv(f'sensor_data_{type_value}.csv', index=False)
    
    
    


