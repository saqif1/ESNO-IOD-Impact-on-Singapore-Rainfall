import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the data into a pandas DataFrame
df = pd.read_csv('df_pr_enso_iod.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Specify the year range for the analysis
start_year = 1980
end_year = 2021

# Subset the data for the specified year range
df_year = df.loc[(df.index.year >= start_year) & (df.index.year <= end_year)]

# Calculate the correlation between precipitation and NINO 3.4 over each year of the time series
corr_nino_yearly = df_year[['Precipitation', 'NINO 3.4 SST Anomalies']].groupby(df_year.index.year).corr().iloc[0::2,-1]

# Calculate the correlation between precipitation and IOD over each year of the time series
corr_iod_yearly = df_year[['Precipitation', 'DMI']].groupby(df_year.index.year).corr().iloc[0::2,-1]

# Print the correlation coefficients for each year
print("Yearly correlation between Precipitation and NINO 3.4:\n", corr_nino_yearly)
print("Yearly correlation between Precipitation and IOD:\n", corr_iod_yearly)

# Create a scatter plot of precipitation vs. NINO 3.4 with regression line and correlation coefficient
fig, ax = plt.subplots()
ax.scatter(df_year['NINO 3.4 SST Anomalies'], df_year['Precipitation'], s=10)
ax.set_xlabel('NINO 3.4 SST Anomalies')
ax.set_ylabel('Precipitation')
ax.set_title(f"Correlation between Singapore's precipitation and NINO 3.4 SST Anomalies ({start_year}-{end_year})")
slope, intercept, r_value, p_value, std_err = stats.linregress(df_year['NINO 3.4 SST Anomalies'], df_year['Precipitation'])
ax.plot(df_year['NINO 3.4 SST Anomalies'], slope * df_year['NINO 3.4 SST Anomalies'] + intercept, color='red')
ax.text(0.05, 0.95, f"r = {r_value:.2f}", transform=ax.transAxes, va='top')

# Create a scatter plot of precipitation vs. IOD with regression line and correlation coefficient
fig, ax = plt.subplots()
ax.scatter(df_year['DMI'], df_year['Precipitation'], s=10)
ax.set_xlabel('IOD')
ax.set_ylabel('Precipitation')
ax.set_title(f"Correlation between Singapore's precipitation and IOD ({start_year}-{end_year})")
slope, intercept, r_value, p_value, std_err = stats.linregress(df_year['DMI'], df_year['Precipitation'])
ax.plot(df_year['DMI'], slope * df_year['DMI'] + intercept, color='red')
ax.text(0.05, 0.95, f"r = {r_value:.2f}", transform=ax.transAxes, va='top')

plt.show()















