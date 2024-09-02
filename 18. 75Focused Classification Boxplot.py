# Import required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_csv('75focused_years_classified.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Specify the year range for the analysis
start_year = 1980
end_year = 2021

# Subset the data for the specified year range
df_year = df.loc[(df.index.year >= start_year) & (df.index.year <= end_year)]

# Create a list of dataframes and their labels
dfs = [df_year.loc[(df_year['ENSO'] == 'EN') & (df_year['IOD'] == '+IOD')],
       df_year.loc[(df_year['ENSO'] == 'EN') & (df_year['IOD'] == '-IOD')],
       df_year.loc[(df_year['ENSO'] == 'EN')],
       df_year.loc[(df_year['IOD'] == '+IOD')],
       df_year.loc[(df_year['ENSO'] == 'Neutral') & (df_year['IOD'] == 'Neutral')],
       df_year.loc[(df_year['IOD'] == '-IOD')],
       df_year.loc[(df_year['ENSO'] == 'LN')],
       df_year.loc[(df_year['ENSO'] == 'LN') & (df_year['IOD'] == '-IOD')],
       df_year.loc[(df_year['ENSO'] == 'LN') & (df_year['IOD'] == '+IOD')]]

# Create a list of labels for the boxplots
labels = ['EN, +IOD', 'EN, -IOD', 'EN', '+IOD', 'Neutral', '-IOD', 'LN', 'LN, -IOD', 'LN, +IOD']

# Create a list of values for the number of years (N) in each boxplot
N_values = [len(dfs[i].index.year.unique()) for i in range(len(dfs))]

# Create a list of precipitation data for each category
precip_data = [dfs[i]['Rainfall Anomaly'] for i in range(len(dfs))]

# Create the boxplot
fig, ax = plt.subplots(figsize=(10, 8))
bp = ax.boxplot(precip_data, labels=labels, showfliers=False, patch_artist=True,
                whiskerprops={'linewidth': 0},
                capprops={'linewidth': 2, 'linestyle': 'None'})

# Set the alpha value of the boxplot patches
for patch in bp['boxes']:
    patch.set(alpha=0.5)

# Add a horizontal grid
ax.yaxis.grid(True)

# Set the y-axis label
ax.set_ylabel('Rainfall anomaly (mm/day)')

# Set the title of the plot
plt.title('Boxplots of Daily Average Precipitation by ENSO and IOD Category')

# Add the number of points (N) to each box
for i in range(len(N_values)):
    x_pos = i + 1
    y_pos = bp['caps'][i * 2].get_ydata()[0]
    ax.text(x_pos, y_pos, f'N = {N_values[i]}', ha='right', va='bottom', fontsize=10)

# Add individual observations to the boxplot
for i, points in enumerate(precip_data):
    x = np.ones(len(points)) * (i+1)
    ax.plot(x, points, '.', alpha=0.4, color='black')

# Show the plot
plt.show()

# Create dummy variables for ENSO and IOD columns
dummy_columns = pd.get_dummies(df_year[['ENSO', 'IOD']], prefix=['ENSO', 'IOD'], drop_first=True)
df_year = pd.concat([df_year, dummy_columns], axis=1)

import statsmodels.api as sm

# Define the independent variables (predictors) and the dependent variable (response)
X = df_year[['ENSO_LN', 'ENSO_Neutral', 'IOD_-IOD', 'IOD_Neutral']]
y = df_year['Rainfall Anomaly']

# Add a constant term to the independent variables (X)
X = sm.add_constant(X)

# Fit the multiple linear regression model
model = sm.OLS(y, X).fit()

# Print the model summary
print(model.summary())

import seaborn as sns

# Create a scatter plot with ENSO on the x-axis, IOD on the y-axis, and Rainfall Anomaly represented by the size of the points
fig, ax = plt.subplots(figsize=(10, 8))
scatter = sns.scatterplot(data=df_year, x='NINO 3.4 SST Anomalies', y='DMI', hue='Year', size='Rainfall Anomaly',
                          sizes=(50, 250), palette='viridis', legend='full', alpha=0.7, ax=ax)

# Set axis labels and title
ax.set_xlabel('NINO 3.4 SST Anomalies')
ax.set_ylabel('DMI')
ax.set_title('Scatter Plot of Rainfall Anomaly in Singapore by ENSO and IOD')

# Set legend title
ax.legend(title='Year')

# Get the median values of each boxplot category
medians = [np.median(d) for d in precip_data]

# Print the median values
for i in range(len(medians)):
    print(f'{labels[i]} median: {medians[i]:.2f} mm/day')

# Show the plot
plt.show()







































