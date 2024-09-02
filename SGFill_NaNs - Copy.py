
import geopandas as gpd
import numpy as np
import pandas as pd


### Print options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

### Load data
datafr = pd.read_csv('Comb_Daily_Pr_Special.csv')

### Station geodataframe
Stn_data = pd.DataFrame(datafr,columns=['id','Longitude','Latitude'])
Stn_data_gdf = gpd.GeoDataFrame(Stn_data, geometry=gpd.points_from_xy(Stn_data.Longitude,Stn_data.Latitude), crs='EPSG:3414')

### Re-make Precipitation array to [id,Date,Rainfall,Stn_name]
dfr = datafr.melt(id_vars=["id","Station","Longitude","Latitude","Elevation"], var_name="Date", value_name="Rainfall (mm)")

### Join gdf and df by 'id'
gdf = pd.merge(left=Stn_data_gdf, right=dfr, how='outer',on='id' )
gdf = gdf.sort_values(['Date','id']).reset_index().drop(columns=['index','Longitude_x', 'Latitude_x', 'Elevation','Longitude_y', 'Latitude_y'])
#df.to_csv('final.csv')

### Applying multi-indexing - FINAL Dataset for filling NaNs
gdf.set_index(['Date','id'], inplace=True)

### sample formatting
s = gdf.loc['19800101'].geometry
point = gdf.loc['19800101'].geometry.iloc[0] #to change for all station in that day.

closest_stn_posindex = s.distance(point).argsort().iloc[1] #choose 2nd elem bcos first is the stn itself.
closest_stn_rainfall = gdf.loc['19800101'].iloc[closest_stn_posindex]['Rainfall (mm)'] #closest stn's rainfall

### Get index of stations with NaN rainfall
nan_rainfall_idx = gdf.index[pd.isna(gdf['Rainfall (mm)'])] #tuple index that has nan rainfall

### Loop attempt
for idx in nan_rainfall_idx:
    year_idx = idx[0]
    stn_idx = idx[1]
    point = gdf.loc[idx].geometry

    s = gdf.loc[year_idx].geometry

    for i in range(len(gdf.loc[year_idx])):
        if (s.distance(point).argsort().iloc[i] > 0) and (pd.isna(gdf.loc[year_idx].iloc[s.distance(point).argsort().iloc[i]]['Rainfall (mm)'])):
            closest_stn_posindex = s.distance(point).argsort().iloc[i]
            closest_stn_rainfall = gdf.loc[year_idx].iloc[closest_stn_posindex]['Rainfall (mm)']
        print(closest_stn_posindex,closest_stn_rainfall)
    gdf.loc[idx]['Rainfall (mm)'] = closest_stn_rainfall

print(gdf)

'''
point = gdf.loc['19800101',8].geometry
s = gdf.loc['19800101'].geometry
#print(s.distance(point).argsort().iloc[1] > 0)
#print(s.distance(point))
#print(s.distance(point).argsort())
#print(gdf.loc['19800101'].iloc[s.distance(point).argsort().iloc[:]]['Rainfall (mm)'])
#print(gdf.loc['19800101'].iloc[s.distance(point).argsort().iloc[1]]['Rainfall (mm)']) #closest rainfall
#print(gdf.loc['19800101',8]['Rainfall (mm)']) #to be replaced
for i in range(len(gdf.loc['19800101'])):
        if (s.distance(point).argsort().iloc[i] > 0) and (pd.notna(gdf.loc['19800101'].iloc[s.distance(point).argsort().iloc[i]]['Rainfall (mm)'])):
            closest_stn_posindex = s.distance(point).argsort().iloc[i]
            closest_stn_rainfall = gdf.loc['19800101'].iloc[closest_stn_posindex]['Rainfall (mm)']

print(gdf.loc['19800101'].iloc[closest_stn_posindex],closest_stn_rainfall)
'''
