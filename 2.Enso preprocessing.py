import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ENSO.csv', parse_dates=[0])
df.replace('NAN',np.nan,inplace=True)

#Limit between 1980 to 2021 and 3.4 index only
df = df.loc[(df.Year>=1980)&(df.Year<=2021)]
df.rename(columns={'Precipitation (mm/day)':'Precipitation'}, inplace=True)

#Set dtypes
df = df.astype({
                'Month': str,
                'Season': str,
                'ONI': float,
                'NINO 1+2 SST': float,
                'NINO 1+2 SST Anomalies': float,
                'NINO 3 SST': float,
                'NINO 3 SST Anomalies': float,
                'NINO 3.4 SST': float,
                'NINO 3.4 SST Anomalies': float,
                'NINO 4 SST': float,
                'NINO 4 SST Anomalies': float,
                'OLR': float,
                'TNI': float,
                'Precipitation': float
             })

#Isolate indicators
indicators = df.iloc[:,4:]

#Replace NaN with monthly mean throughout 1980-2021
mean_month = df.groupby('Month')[df.columns[4:]].transform(np.mean)
df.fillna(mean_month, inplace=True)

df = df[['Date','Year','Month','NINO 3.4 SST Anomalies']]
#df.to_csv('ENSO_adj.csv')







#Plot Nino 3.4 SST Anomalies
#print(df.columns)
plt.figure(figsize=(15,5))
plt.title("Chart of 'NINO 3.4 SST Anomalies' VS. Time")
#plt.axhline(y=0.5720203369083314, color='r', linestyle='--', label='El Niño threshold')
#plt.axhline(y=-0.5720203369083314, color='b', linestyle='--', label='La Niña threshold') #threshold from http://www.bom.gov.au/climate/enso/indices/about.shtml
sns.lineplot(x='Date', y='NINO 3.4 SST Anomalies', data=df)
#plt.fill_between(df['Date'], df['NINO 3.4 SST Anomalies'], 0.8, where=df['NINO 3.4 SST Anomalies']>=0.8, interpolate=True, color='red')
#plt.fill_between(df['Date'], df['NINO 3.4 SST Anomalies'], -0.8, where=df['NINO 3.4 SST Anomalies']<=-0.8, interpolate=True, color='blue')
plt.ylabel('°C above or below average')
plt.xlabel('Year')
plt.legend()
plt.show()
