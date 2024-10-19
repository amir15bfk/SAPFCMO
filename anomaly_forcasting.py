import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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





# Load and preprocess historical data for a given machine type
def load_and_preprocess_data(machine_type):
    file_paths = {
        'WELDING': 'sensor_data_WELDING.csv',
        'STAMPING': 'sensor_data_STAMPING.csv',
        'AGV': 'sensor_data_AGV.csv',
        'LEAK_TEST': 'sensor_data_LEAK_TEST.csv',
        'PAINTING': 'sensor_data_PAINTING.csv',
        'CNC': 'sensor_data_CNC.csv'
    }
    
    if machine_type not in file_paths:
        raise ValueError(f"Unknown machine type: {machine_type}")
    
    file_path = file_paths[machine_type]
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    return df

# Helper function for Exponential Smoothing forecasting
def exponential_smoothing_forecast(series, steps):
    model = ExponentialSmoothing(series, trend='add', seasonal='add', seasonal_periods=24)
    results = model.fit()
    forecast = results.forecast(steps=steps)
    return forecast

# Function to forecast for a specific machine type, column, and period
def forecast_machine_data(machine_type, column, period=168):
    df = load_and_preprocess_data(machine_type)
    
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in data for machine type {machine_type}")
    
    train = df[column]
    
    forecast = exponential_smoothing_forecast(train, period)
    
    # Create a new index for the forecasted period
    last_timestamp = train.index[-1]
    forecast_index = pd.date_range(start=last_timestamp, periods=period + 1, freq='H')[1:] 
    return forecast, forecast_index

# Function to plot the forecasted data
def plot_forecast(train, forecast, forecast_index, column):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast_index, forecast, label='Forecast', color='red')
    ax.set_title(f"Forecasting for {column}")
    ax.legend()
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(column)
    plt.tight_layout()
    plt.show()



# Example usage
#machine_type = 'WELDING'
#column = 'pressure_applied'
#period = 168  # One week
#
#train = load_and_preprocess_data(machine_type)[column]
#forecast, forecast_index = forecast_machine_data(machine_type, column, period)
#
#plot_forecast(train, forecast, forecast_index, column)