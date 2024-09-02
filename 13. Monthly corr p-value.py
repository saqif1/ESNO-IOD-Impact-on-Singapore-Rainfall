# Import required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load the data into a pandas DataFrame
df = pd.read_csv('df_pr_enso_iod.csv')

# Set up data for plotting
months = np.arange(1, 13)
corr_monthly_rainfall_nino = []
pval_monthly_rainfall_nino = []
corr_monthly_rainfall_dmi = []
pval_monthly_rainfall_dmi = []

for month in range(1, 13):
    monthly_rainfall = df[df['Month'] == month]['Daily Average Precipitation']
    nino_values = df[df['Month'] == month]['NINO 3.4 SST Anomalies']
    dmi_values = df[df['Month'] == month]['DMI']

    # Calculate correlation and p-value for NINO 3.4 SST Anomalies
    corr_nino, pval_nino = pearsonr(monthly_rainfall, nino_values)
    corr_monthly_rainfall_nino.append(corr_nino)
    pval_monthly_rainfall_nino.append(pval_nino)

    # Calculate correlation and p-value for DMI
    corr_dmi, pval_dmi = pearsonr(monthly_rainfall, dmi_values)
    corr_monthly_rainfall_dmi.append(corr_dmi)
    pval_monthly_rainfall_dmi.append(pval_dmi)

# Create a bar chart for correlation coefficients and p-values
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.35
ax.bar(months - width / 2, corr_monthly_rainfall_nino, width, label='NINO 3.4 SST Anomalies')
ax.bar(months + width / 2, corr_monthly_rainfall_dmi, width, label='DMI')
ax.set_xticks(months)
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.set_ylabel('Correlation Coefficient')
ax.set_xlabel('Month')
ax.set_title('Daily Average Rainfall Correlation with NINO 3.4 SST Anomalies and DMI by Month')
ax.legend()

# Add correlation coefficients and p-values as annotations
for i, pval in enumerate(pval_monthly_rainfall_nino):
    if pval < 0.01:
        ax.annotate('r={:.3f}\np={:.3f}'.format(corr_monthly_rainfall_nino[i], pval), (i+0.55, corr_monthly_rainfall_nino[i]+0.05), fontsize=8, color='red')
    elif pval < 0.05:
        ax.annotate('r={:.3f}\np={:.3f}'.format(corr_monthly_rainfall_nino[i], pval), (i+0.55, corr_monthly_rainfall_nino[i]+0.05), fontsize=8, color='black')
for i, pval in enumerate(pval_monthly_rainfall_dmi):
    if pval < 0.01:
        ax.annotate('r={:.3f}\np={:.3f}'.format(corr_monthly_rainfall_dmi[i], pval), (i+0.95, corr_monthly_rainfall_dmi[i]+0.05), fontsize=8, color='red')
    elif pval < 0.05:
        ax.annotate('r={:.3f}\np={:.3f}'.format(corr_monthly_rainfall_dmi[i], pval), (i+0.95, corr_monthly_rainfall_dmi[i]+0.05), fontsize=8, color='black')


# Add a black horizontal line at y=0
ax.axhline(y=0, color='black')

plt.show()


































