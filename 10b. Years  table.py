import pandas as pd
import numpy as np

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

# Resample the DataFrame to yearly frequency and take the mean of each year
df_year = df_year.resample('Y').mean()

# Drop the 'Unnamed: 0', 'Month', and 'Year' columns
df_year.drop(['Unnamed: 0', 'Month', 'Year'], axis=1, inplace=True)

# Calculate the standard deviations of the NINO 3.4 SST Anomalies and DMI columns
nino_sd = df_year['NINO 3.4 SST Anomalies'].std()
dmi_sd = df_year['DMI'].std()

# Create a new column for ENSO classifications based on +1 standard deviation of NINO 3.4 SST Anomalies
df_year['ENSO'] = pd.cut(df_year['NINO 3.4 SST Anomalies'], bins=[-np.inf, -nino_sd, nino_sd, np.inf], labels=['LN', 'Neutral', 'EN'])

# Create a new column for IOD classifications based on +1 standard deviation of DMI
df_year['IOD'] = pd.cut(df_year['DMI'], bins=[-np.inf, -dmi_sd, dmi_sd, np.inf], labels=['-IOD', 'Neutral', '+IOD'])

# Pivot the table to get the count of years for each ENSO-IOD combination
years_table = pd.pivot_table(df_year, values='Daily Average Precipitation', index='IOD', columns='ENSO', aggfunc=lambda x: ', '.join(x.index.year.astype(str)))

# Write the pivot table to a CSV file
#years_table.to_csv('years_table.csv', index_label='IOD')
print(years_table)






























