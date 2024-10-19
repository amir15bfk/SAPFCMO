import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import IsolationForest

import os
import django
import pandas as pd
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SAPFCMO.settings')
django.setup()


from webhook_handler.models import SensorData
from webhook_handler.models import Machine
from webhook_handler.models import LatestSensorData


file_paths = {
    'WELDING': 'sensor_data_WELDING.csv',
    'STAMPING': 'sensor_data_STAMPING.csv',
    'AGV': 'sensor_data_AGV.csv',
    'CNC': 'sensor_data_CNC.csv',
    'PAINTING': 'sensor_data_PAINTING.csv',
    'LEAK_TEST': 'sensor_data_LEAK_TEST.csv'
}

# Load and preprocess historical data for a given machine type
def load_and_preprocess_data(machine_type):
    
    
    file_path = file_paths[machine_type]
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df




# Anomaly detection function for a new incoming data point
def detect_anomaly_for_point(data_point, machine_type, contamination=0.005):
    # Load historical data for the machine type
    df = load_and_preprocess_data(machine_type)
    
    # Select only numerical columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Convert the new data point to a DataFrame and select only numeric columns
    new_df = pd.DataFrame(data_point, index=[pd.Timestamp.now()])
    new_df = new_df.select_dtypes(include=[np.number])
    
    # Combine the historical data with the new data point
    combined_df = pd.concat([numeric_df, new_df], axis=0)
    
    # Scale the data
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(combined_df)

    # Perform general anomaly detection across all columns
    clf_general = IsolationForest(contamination=contamination, random_state=42)
    y_pred_general = clf_general.fit_predict(X_scaled)
    is_general_anomaly = y_pred_general[-1] == -1  # Check if the new point is a general anomaly

    # Perform per-column anomaly detection
    column_anomalies = {}
    for column in numeric_df.columns:
        clf_column = IsolationForest(contamination=contamination, random_state=42)
        y_pred_column = clf_column.fit_predict(X_scaled[:, numeric_df.columns.get_loc(column)].reshape(-1, 1))
        column_anomalies[column] = y_pred_column[-1] == -1  # Check if the new point is an anomaly for this column
    
    # Extract the columns where anomalies are detected
    anomaly_columns = [col for col, is_anomaly in column_anomalies.items() if is_anomaly]

    return {
        'is_general_anomaly': is_general_anomaly,
        'anomaly_columns': anomaly_columns
    }   
    
    
    
    

    

    
 
def process_new_data_point(data_point, machine):
    # Flatten the data point
    flattened_data = {
        'Machine': machine,
        'Type': machine.machine_type,
        'Machine ID': machine.machine_id,
        'Timestamp': pd.Timestamp.now(),
        **data_point
    }
    
    # Handle nested structures
    if 'arm_position' in flattened_data:
        flattened_data['x'] = flattened_data['arm_position'].get('x')
        flattened_data['y'] = flattened_data['arm_position'].get('y')
        flattened_data['z'] = flattened_data['arm_position'].get('z')
        del flattened_data['arm_position']
        
    if 'location' in flattened_data:
        flattened_data['x'] = flattened_data['location'].get('x')
        flattened_data['y'] = flattened_data['location'].get('y')
        flattened_data['z'] = flattened_data['location'].get('z')
        del flattened_data['location']
    
    return flattened_data



# Update the check_anomalies_for_all_machines function
def check_anomalies_for_all_machines():
    machine_types = LatestSensorData.objects.values_list('machine__machine_type', flat=True).distinct()
    
    for machine_type in machine_types:
        latest_data = LatestSensorData.objects.filter(machine__machine_type=machine_type).latest('timestamp')
        new_data_point = latest_data.data
        machine = latest_data.machine
        
        # Process the new data point
        processed_data_point = process_new_data_point(new_data_point, machine)
        
        anomaly_result = detect_anomaly_for_point(processed_data_point, machine_type)
        
        print(f"Machine Type: {machine_type}")
        print(f"General Anomaly: {anomaly_result['is_general_anomaly']}")
        if anomaly_result['anomaly_columns']:
            print(f"Anomalous Columns: {', '.join(anomaly_result['anomaly_columns'])}")
        else:
            print("No specific column anomalies detected.")
        print("")

# Call the function to check anomalies for all machine types
# check_anomalies_for_all_machines()
