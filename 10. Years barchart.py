import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_csv('years_classified.csv')

# Convert the 'Date' column to datetime and set it as the index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Create a figure with one subplot
fig, ax = plt.subplots(figsize=(10, 8))

# Subset the data for ENSO and IOD
enso_data = df[df['ENSO'].isin(['EN', 'LN'])]
iod_data = df[df['IOD'].isin(['+IOD', '-IOD'])]

# Get the unique years in the data
years = np.unique(df.index.year)

# Compute the total ENSO and IOD values for each year
enso_totals = [enso_data.loc[enso_data.index.year == year, 'NINO 3.4 SST Anomalies'].sum() for year in years]
iod_totals = [iod_data.loc[iod_data.index.year == year, 'DMI'].sum() for year in years]

# Plot the stacked bar chart
ax.bar(years, enso_totals, color='blue', label='ENSO')
ax.bar(years, iod_totals, bottom=enso_totals, color='red', label='IOD')

# Set the title and labels for the subplot
ax.set_title("Historical record of IOD and ENSO years")
ax.set_xlabel('Year')
ax.set_ylabel('Anomalies')

# Add a legend
ax.legend()

# Set x-ticks and labels vertically
ax.set_xticks(years)
ax.set_xticklabels(years, rotation='vertical')

# Add horizontal line
ax.axhline(y=0, color='black')

# Show the plot
plt.show()






























