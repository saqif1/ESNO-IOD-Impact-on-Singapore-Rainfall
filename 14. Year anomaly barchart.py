import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_csv('years_classified.csv')

# Convert the 'Date' column to datetime and set it as the index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Create a figure with two subplots that share the same x-axis
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

# Subset the data for ENSO and IOD
enso_data = df[df['ENSO'].isin(['EN', 'LN'])]
iod_data = df[df['IOD'].isin(['+IOD', '-IOD'])]

# Get the unique years in the data
years = np.unique(df.index.year)

# Compute the total ENSO and IOD values for each year
enso_totals = [enso_data.loc[enso_data.index.year == year, 'NINO 3.4 SST Anomalies'].sum() for year in years]
iod_totals = [iod_data.loc[iod_data.index.year == year, 'DMI'].sum() for year in years]

# Plot the stacked bar chart for the first subplot
ax1.bar(years, enso_totals, color='blue', label='ENSO')
ax1.bar(years, iod_totals, bottom=enso_totals, color='red', label='IOD')

# Set the title and labels for the first subplot
ax1.set_title("Historical record of IOD and ENSO years")
ax1.set_ylabel('Anomalies')

# Add a legend to the first subplot
ax1.legend()

# Add a horizontal line to the first subplot
ax1.axhline(y=0, color='black')

# Plot the bar chart for the second subplot
ax2.bar(df.index.year, df['Rainfall Anomaly'])

# Set the title and labels for the second subplot
ax2.set_title('Rainfall Anomaly by Year')
ax2.set_xlabel('Year')
ax2.set_ylabel('Rainfall Anomaly (%)')

# Add x-axis tick marks for every year
ax2.set_xticks(years)

# Set x-axis tick labels for every year
ax2.set_xticklabels([str(year) for year in years])

# Rotate tick labels by 90 degrees to prevent overlap
ax2.xaxis.set_tick_params(rotation=90)

# Add a horizontal line to the second subplot
ax2.axhline(y=0, color='black')

# Show the plot
plt.show()






































