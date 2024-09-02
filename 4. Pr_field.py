import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Date converter function; Day 0 = 1 January 1980
def convert_days_to_datetime(days):
    return pd.Timestamp('1980-01-01') + pd.Timedelta(days=days)

# Open file
data = xr.open_dataset('Precipitation_Singapore_Grid.nc')

# Convert nc to df
df = data.to_dataframe()

# Drop unnecessary data
df = df.drop(['Date','X_coordinates', 'Y_coordinates'], axis=1)

# Convert day index to datetime
df.index = df.index.set_levels(df.index.levels[2].map(convert_days_to_datetime), level='Time')

# Downcast to save memory
df['Precipitation'] = df['Precipitation'].astype('float16')

# Extract month and year from Time index
df['Month'] = df.index.get_level_values('Time').month
df['Year'] = df.index.get_level_values('Time').year

# Group data by month and year and calculate mean precipitation
df_monthly = df.groupby(['Year', 'Month'])[['Precipitation']].mean()




