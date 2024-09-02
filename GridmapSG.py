import numpy as np
import pandas as pd

### Load data
datafr = pd.read_csv('Combined Daily Pr.csv')

### Parameters
Stn_code = datafr['id'].to_numpy() #Stn code number
Stn_name = datafr['Station'].to_numpy()
Long = datafr['Longitude'].to_numpy() #Longitude in wgs84
Lat = datafr['Latitude'].to_numpy() #Latitude in wgs84
Elev = datafr['Elevation'].to_numpy() #Latitude in Svy21
Dates = np.array(datafr.columns[5:]) #Date in format: no.of days since 1-January-0000

import requests, itertools, io
from pathlib import Path
import urllib
from zipfile import ZipFile
import fiona.drvsupport
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry
import webbrowser
from plotly.offline import plot

# get official Singapore planning area geometry
url = "https://geo.data.gov.sg/planning-area-census2010/2014/04/14/kml/planning-area-census2010.zip"

f = Path.cwd().joinpath(urllib.parse.urlparse(url).path.split("/")[-1])
if not f.exists():
    r = requests.get(url, stream=True, headers={"User-Agent": "XY"})
    with open(f, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
zfile = ZipFile(f)
zfile.extractall(f.stem)

fiona.drvsupport.supported_drivers['KML'] = 'rw'
gdf_sg = gpd.read_file([_ for _ in Path.cwd().joinpath(f.stem).glob("*.kml")][0], driver="KML") #Singapore area geometry

# get data about Singapore weather stations
df_stations = pd.DataFrame({"id": Stn_code, "name": Stn_name, "location.latitude": Lat,"location.longitude": Long }) #recreate new array with header

# Re-make Precipitation array to [id,Date,Rainfall,Stn_name]
df = datafr.melt(id_vars=["id","Station","Longitude","Latitude","Elevation"], var_name="Date", value_name="Rainfall (mm)") #to restructure the dataframe cannot leave any header blank categorise them correctly

# number of meters
STEP = 1000 #grid resolution size in nxn m
a, b, c, d = gdf_sg.to_crs(gdf_sg.estimate_utm_crs()).total_bounds #return minx, miny, maxx,maxy in this order to establish rectangular boundary

# create a grid for Singapore
gdf_grid = gpd.GeoDataFrame(
    geometry=[
        shapely.geometry.box(minx, miny, maxx, maxy)
        for minx, maxx in zip(np.arange(a, c, STEP), np.arange(a, c, STEP)[1:])
        for miny, maxy in zip(np.arange(b, d, STEP), np.arange(b, d, STEP)[1:])
    ],
    crs=gdf_sg.estimate_utm_crs(),
).to_crs(gdf_sg.crs)

# restrict grid to only squares that intersect with Singapore geometry
gdf_grid = (
    gdf_grid.sjoin(gdf_sg)
    .pipe(lambda d: d.groupby(d.index).first())
    .set_crs(gdf_grid.crs)
    .drop(columns=["index_right"])
)

# geodataframe of weather station locations and rainfall by date
gdf_rainfall = gpd.GeoDataFrame(
    df.merge(df_stations, on="id")
    .assign(
        geometry=lambda d: gpd.points_from_xy(
            d["location.longitude"], d["location.latitude"]
        )
    )
    .drop(columns=["location.latitude", "location.longitude","Longitude","Latitude","Elevation"]),
    crs=gdf_sg.crs,
).sort_values('Date') #Add lat and lon columns into 1 coordinate. Then, remove the .drop individual columns
#print(gdf_rainfall.loc[gdf_rainfall.Date=='19800101']['Rainfall (mm)'])

# nearest rainfall station to grid mapping
gdf_grid_rainfall = gpd.sjoin_nearest(gdf_grid, gdf_rainfall).drop(columns=["Description", "index_right"])### .fillna=0???
#print(gdf_grid_rainfall.columns)
print(pd.isna(gdf_grid_rainfall))

'''
# visualize map with folium
sg_gridded_snap = gdf_grid_rainfall.loc[lambda d: d["Date"].eq("20211231")].explore("Rainfall (mm)", height=400, width=600)
output_file = "map.html"
sg_gridded_snap.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab
'''

'''
# visualisation by plotly animation
import plotly.express as px

# reduce dates so figure builds in sensible time
gdf_px = gdf_grid_rainfall.loc[
    lambda d: d["Date"].isin(
        gdf_grid_rainfall["Date"].value_counts().sort_index().index[0:10]
    )
]

sg_gridded = px.choropleth_mapbox(
    gdf_px,
    geojson=gdf_px.geometry,
    locations=gdf_px.index,
    color="Rainfall (mm)",
    hover_data=gdf_px.columns[1:].tolist(),
    animation_frame="Date",
    mapbox_style="carto-positron",
    center={"lat":gdf_px.unary_union.centroid.y, "lon":gdf_px.unary_union.centroid.x},
    zoom=8.5
).update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 4})

plot(sg_gridded)
'''

