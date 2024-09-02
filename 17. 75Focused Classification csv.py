import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_csv('df_pr_enso_iod.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Specify the date range for the analysis
start_year = 1980
end_year = 2021
start_month = 6
end_month = 10

# Subset the data for the specified date range
df_date = df.loc[(df.index.year >= start_year) & (df.index.year <= end_year) &
                 (df.index.month >= start_month) & (df.index.month <= end_month)]

# Resample the DataFrame to yearly frequency and take the mean of each year
df_year = df_date.resample('Y').mean()

# Drop the 'Unnamed: 0', 'Month', and 'Year' columns
df_year.drop(['Unnamed: 0', 'Month', 'Year'], axis=1, inplace=True)

# Calculate the standard deviations of the NINO 3.4 SST Anomalies and DMI columns
nino_sd = df_year['NINO 3.4 SST Anomalies'].std()
dmi_sd = df_year['DMI'].std()

# Create a new column for ENSO classifications based on +1 standard deviation of NINO 3.4 SST Anomalies
df_year['ENSO'] = np.where(df_year['NINO 3.4 SST Anomalies'] > 0.75*nino_sd, 'EN',
                            np.where(df_year['NINO 3.4 SST Anomalies'] < -0.75*nino_sd, 'LN', 'Neutral'))

# Create a new column for IOD classifications based on +1 standard deviation of DMI
df_year['IOD'] = np.where(df_year['DMI'] > 0.75*dmi_sd, '+IOD',
                           np.where(df_year['DMI'] < -0.75*dmi_sd, '-IOD', 'Neutral'))

# Calculate the long-term average precipitation
long_term_avg_precip = df['Daily Average Precipitation'].mean()

# Calculate the Rainfall Anomaly as a departure from the long-term average
df_year['Rainfall Anomaly'] = (df_year['Daily Average Precipitation'] - long_term_avg_precip)

# Create a column 'Year' from the index
df_year['Year'] = df_year.index.year

# Create a pivot table with ENSO classifications as columns and IOD classifications as rows
pivot_table = df_year.pivot_table(index='IOD', columns='ENSO', values='Year', aggfunc=lambda x: ', '.join(map(str, x)))



#Save the pivot table to a CSV file
#pivot_table.to_csv('75focused_pivot_table_enso_iod.csv')
print(pivot_table)
#print("The +0.75SD value for NINO 3.4 SST Anomalies is:", 0.75*nino_sd)
#print("The 0.75SD value for DMI is:", 0.75*dmi_sd)

#print(df_year.columns)
#df_year.to_csv('75focused_years_classified.csv')





































