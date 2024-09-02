'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io as sio

df = pd.read_csv('IOD.csv')
df = pd.melt(df, id_vars='Year', var_name='Month', value_name='DMI')
df.astype({
    'Month': 'str'
})
df = df.loc[(df.Year>=1980)&(df.Year<=2021)]
df['Date'] = pd.to_datetime(df.Month.astype(str)+'/'+df.Year.astype(str))

df.to_csv('IOD_adj.csv')
#print(df.sort_values('Date').tail())


#Plot DMI
plt.figure(figsize=(15,5))
plt.title("Chart of 'Dipole Mode Index (DMI)' VS. Time")
sns.lineplot(x='Date', y='DMI', data=df)
#plt.axhline(y=0.4,color='r',linestyle='--', label='Positive IOD threshold')
#plt.axhline(y=-0.4,color='b',linestyle='--', label='Negative IOD threshold') #threshold from http://www.bom.gov.au/climate/enso/indices/about.shtml
plt.ylabel('IOD-DMI(°C)')
plt.xlabel('Year')
plt.legend()
plt.show()
'''
import matplotlib.pyplot as plt
import seaborn as sns

# Data
data = {
    "Variable": ["ENSO_EN", "ENSO_LN", "IOD_-IOD", "IOD_+IOD", "Neutral"],
    "Rainfall Anomaly (mm/day)": [0.8569, 0.5, 0.3382, 0.25, 0.1],
    "p-value": [0.001, 0.15, 0.018, 0.3, 0.4],
}

# Create a DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Create the bar plot
plt.figure(figsize=(10, 6))
barplot = sns.barplot(x="Variable", y="Rainfall Anomaly (mm/day)", data=df)

# Add p-values and asterisks for statistical significance at the top of each bar
for i, row in df.iterrows():
    barplot.text(
        i,
        row["Rainfall Anomaly (mm/day)"],
        f'p-value = {row["p-value"]:.3f}',
        ha="center",
        va="bottom",
        fontweight="bold",
        color="black",
    )


# Set plot title and labels
plt.title("Effect of ENSO and IOD Events on Rainfall Anomaly")
plt.xlabel("Phenomenon")
plt.ylabel("Absolute Rainfall Anomaly (mm/day)")

# Show the plot
plt.show()
