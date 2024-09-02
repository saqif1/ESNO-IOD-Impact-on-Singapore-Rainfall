import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the data into a pandas DataFrame
df = pd.read_csv('df_pr_enso_iod.csv')
print(df.columns)
# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Specify the year range for the analysis
start_year = 1980
end_year = 2021

# Subset the data for the specified year range
df_year = df.loc[(df.index.year >= start_year) & (df.index.year <= end_year)]

# Calculate the correlation between precipitation and NINO 3.4 over each month of the year
corr_nino_monthly = df_year[['Daily Average Precipitation', 'NINO 3.4 SST Anomalies']].groupby(df_year.index.month).corr().iloc[0::2,-1]

# Calculate the correlation between precipitation and IOD over each month of the year
corr_iod_monthly = df_year[['Daily Average Precipitation', 'DMI']].groupby(df_year.index.month).corr().iloc[0::2,-1]

# Reshape the correlation dataframes to a matrix form for heatmap plotting
corr_nino_matrix = corr_nino_monthly.values.reshape(12,1)
corr_iod_matrix = corr_iod_monthly.values.reshape(12,1)

# Create a heatmap of the correlation coefficients for each month
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(corr_nino_matrix, cmap='coolwarm', annot=True, cbar=False, yticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], annot_kws={'fontsize': 12})
ax.set_xlabel('NINO 3.4 SST Anomalies', fontsize=14)
ax.set_ylabel('Month', fontsize=14)
ax.set_title(f"Correlation between Singapore's precipitation and NINO 3.4 SST Anomalies ({start_year}-{end_year})", fontsize=16)

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(corr_iod_matrix, cmap='coolwarm', annot=True, cbar=False, yticklabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], annot_kws={'fontsize': 12})
ax.set_xlabel('IOD', fontsize=14)
ax.set_ylabel('Month', fontsize=14)
ax.set_title(f"Correlation between Singapore's precipitation and IOD ({start_year}-{end_year})", fontsize=16)

plt.show()

















