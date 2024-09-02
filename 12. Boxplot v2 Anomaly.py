# Import required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the data into a pandas DataFrame
df = pd.read_csv('years_classified.csv')

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
       df_year.loc[(df_year['ENSO'] == 'EN') & (df_year['IOD'] == 'Neutral')],
       df_year.loc[(df_year['ENSO'] == 'Neutral') & (df_year['IOD'] == '+IOD')],
       df_year.loc[(df_year['ENSO'] == 'Neutral') & (df_year['IOD'] == 'Neutral')],
       df_year.loc[(df_year['ENSO'] == 'Neutral') & (df_year['IOD'] == '-IOD')],
       df_year.loc[(df_year['ENSO'] == 'LN') & (df_year['IOD'] == 'Neutral')],
       df_year.loc[(df_year['ENSO'] == 'LN') & (df_year['IOD'] == '-IOD')]]

# Create a list of labels for the boxplots
labels = ['EN, +IOD', 'EN', '+IOD', 'Neutral', '-IOD', 'LN', 'LN, -IOD']

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
ax.set_ylabel('Rainfall Anomaly (%)')

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

#Print year data
table = pd.pivot_table(df_year, values='Date', index=['IOD'], columns=['ENSO'], aggfunc=np.sum)
print(table)



































