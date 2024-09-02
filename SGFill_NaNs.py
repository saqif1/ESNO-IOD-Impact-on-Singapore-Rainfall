import requests, itertools, io
from pathlib import Path
import urllib
from zipfile import ZipFile
import fiona.drvsupport
import shapely.geometry
import webbrowser
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

### Join gdf and dfr by 'id'
gdf = pd.merge(left=Stn_data_gdf, right=dfr, how='outer',on='id' )
gdf = gdf.sort_values(['Date','id']).reset_index().drop(columns=['index','Longitude_x', 'Latitude_x', 'Elevation','Longitude_y', 'Latitude_y'])
#df.to_csv('final.csv')

### Applying multi-indexing - FINAL Dataset for filling NaNs
gdf.set_index(['Date','id'], inplace=True)

### Drop rows with NaN
gdf = gdf.dropna().to_crs('4326').reset_index()

### Make grid of Singapore
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

# Number of meters for grid
STEP = 1000 #grid resolution size in nxn m
a, b, c, d = gdf_sg.to_crs(gdf_sg.estimate_utm_crs()).total_bounds #return minx, miny, maxx,maxy in this order to establish rectangular boundary

# Create a grid for Singapore
gdf_grid = gpd.GeoDataFrame(
    geometry=[
        shapely.geometry.box(minx, miny, maxx, maxy)
        for minx, maxx in zip(np.arange(a, c, STEP), np.arange(a, c, STEP)[1:])
        for miny, maxy in zip(np.arange(b, d, STEP), np.arange(b, d, STEP)[1:])
    ],
    crs=gdf_sg.estimate_utm_crs(),
).to_crs(gdf_sg.crs)

# Restrict grid to only squares that intersect with Singapore geometry
gdf_grid = (
    gdf_grid.sjoin(gdf_sg)
    .pipe(lambda d: d.groupby(d.index).first())
    .set_crs(gdf_grid.crs)
    .drop(columns=["index_right"])
)

### Join the gdf_grid to gdf rainfall datas
gdf_grid_rainfall = gpd.sjoin_nearest(gdf_grid, gdf).drop(columns=['Description', 'index_right'])
print(gdf_grid_rainfall)
'''
### Visualize map with folium
sg_gridded_snap = gdf_grid_rainfall.loc[lambda d: d["Date"].eq("20211231")].explore("Rainfall (mm)", height=400, width=600)
output_file = "FINAL_map.html"
sg_gridded_snap.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab
'''
