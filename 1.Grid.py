'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio


### Load file
mat = sio.loadmat('SINGAPORE_GRID.mat') #Singapore grid
mat_pr = sio.loadmat('Daily_Meteo_SG.mat') #Precipitation data

### mat Keys
dtm = mat['DTM']
landcover = mat['Land_Cover']
mask = mat['MASK']
cellsize = mat['cellsize']
lat = mat['lat']
lon = mat['lon']
x = mat['x']
xllcorner = mat['xllcorner']
y = mat['y']
yllcorner = mat['yllcorner']

### pr Keys
stn_code = mat_pr['Code']
Date = mat_pr['Date']
elevn = mat_pr['Ele']
Lat = mat_pr['Lat']
Lon = mat_pr['Lon']
pr = mat_pr['Pr_All']
none = mat_pr['None']
stn_name = mat_pr['Station_Name']
xsta = mat_pr['xSta']
ysta = mat_pr['ySta']
print(pr.size)
'''

import matplotlib.pyplot as plt
import seaborn as sns

# Data
data = {
    "Variable": ["ENSO_EN", "IOD_-IOD"],
    "Rainfall Anomaly (mm/day)": [0.8569, 0.3382],
    "p-value": [0.001, 0.018],
}

# Create a DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Create the bar plot
plt.figure(figsize=(8, 6))
barplot = sns.barplot(x="Variable", y="Rainfall Anomaly (mm/day)", data=df)

# Add p-values at the top of each bar
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
plt.ylabel(" Absolute Rainfall Anomaly (mm/day)")

# Show the plot
plt.show()
