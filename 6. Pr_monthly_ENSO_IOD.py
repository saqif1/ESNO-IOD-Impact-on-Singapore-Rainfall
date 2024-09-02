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
df_monthly = df.groupby(['Year', 'Month'], as_index=False)['Precipitation'].mean()

# Create a new column that combines Year and Month into a single datetime object
df_monthly['Date'] = pd.to_datetime(df_monthly[['Year', 'Month']].assign(DAY=1))

### ENSO
# Open ENSO file
df_enso = pd.read_csv('ENSO_adj.csv', parse_dates=['Date'])

# Merge df_enso and df_precip_monthly
df_pr_enso = pd.merge(left=df_monthly, right=df_enso[['Date','NINO 3.4 SST Anomalies']], on='Date')

### IOD
# Open IOD file
df_iod = pd.read_csv('IOD_adj.csv', parse_dates=['Date'])

# Merge df_enso and df_precip_monthly
df_pr_enso_iod = pd.merge(left=df_pr_enso, right=df_iod[['Date','DMI']], on='Date')
df_pr_enso_iod = df_pr_enso_iod[['Year','Month','Date','Precipitation','NINO 3.4 SST Anomalies', 'DMI']]

# Final downcast
df_pr_enso_iod = df_pr_enso_iod.astype({
                'Year': np.int32,
                'Month': np.int32,
                'NINO 3.4 SST Anomalies': np.float16,
                'DMI' : np.float16})

df_pr_enso_iod.to_csv('df_pr_enso_iod.csv')















