import requests, itertools, io
from pathlib import Path
import urllib
from zipfile import ZipFile
import fiona.drvsupport
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry
from plotly.offline import plot
import webbrowser

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
gdf_sg = gpd.read_file(
    [_ for _ in Path.cwd().joinpath(f.stem).glob("*.kml")][0], driver="KML"
)


# get data about Singapore weather stations
df_stations = pd.json_normalize( #to normalize api format to readable format
    requests.get("https://api.data.gov.sg/v1/environment/rainfall").json()["metadata"]["stations"]) #slicing web-api to get station datas

# dates to get data from weather.gov.sg
dates = pd.date_range("20220601", "20220730", freq="MS").strftime("%Y%m") #convert YYYYMMDD to YYYYMM
df = pd.DataFrame() #empty panda array
# fmt: off
bad = ['S100', 'S201', 'S202', 'S203', 'S204', 'S205', 'S207', 'S208',
       'S209', 'S211', 'S212', 'S213', 'S214', 'S215', 'S216', 'S217',
       'S218', 'S219', 'S220', 'S221', 'S222', 'S223', 'S224', 'S226',
       'S227', 'S228', 'S229', 'S230', 'S900', 'S210']
# fmt: on
for stat, month in itertools.product(df_stations["id"], dates):
    if not stat in bad:
        try:
            df_ = pd.read_csv(
                io.StringIO(
                    requests.get(
                        f"http://www.weather.gov.sg/files/dailydata/DAILYDATA_{stat}_{month}.csv"
                    ).text
                )
            ).iloc[:, 0:5]
        except pd.errors.ParserError as e:
            bad.append(stat)
            print(f"failed {stat} {month}")
        df = pd.concat([df, df_.assign(id=stat)])

df["Rainfall (mm)"] = pd.to_numeric(df["Daily Rainfall Total (mm)"], errors="coerce") #to remove NaN
df["Date"] = pd.to_datetime(df[["Year","Month","Day"]]).dt.strftime("%Y%m%d")
df = df.loc[:,["id","Date","Rainfall (mm)", "Station"]] #rearranging data through python to organise a desirable dataframe with headers needed

# number of meters
STEP = 5000 #grid resolution size in nxn m
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
    df_stations.merge(df, on="id")
    .assign(
        geometry=lambda d: gpd.points_from_xy(
            d["location.longitude"], d["location.latitude"]
        )
    )
    .drop(columns=["location.latitude", "location.longitude"]),
    crs=gdf_sg.crs,
)

# weather station to nearest grid
gdf_grid_rainfall = gpd.sjoin_nearest(gdf_grid, gdf_rainfall).drop(
    columns=["Description", "index_right"]
)
print(gdf_rainfall)

'''
# does it work?  let's visualize with folium
sg_gridded_snap = gdf_grid_rainfall.loc[lambda d: d["Date"].eq("20220622")].explore("Rainfall (mm)", height=400, width=600)
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
        gdf_grid_rainfall["Date"].value_counts().sort_index().index[0:15]
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