import shapely.geometry, shapely.ops
import geopandas as gpd
import numpy as np
import pandas as pd

import webbrowser

# get data from google docs, the slow bit!!!!
df_ = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vS2ijDtnQnbjVhKO1n-9QcIWz2DTPIAxZ7GcIKzNdxEDlxDD6HOO0kITMBDv0sXOTuvLVDnBhx34DIv/pub?gid=186097297&single=true&output=csv")

gdf_sg = gpd.read_file("https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson")

# Singapore bounday as a shapely multipolygon
sg = gdf_sg.dissolve()["geometry"].values[0]
utm = gdf_sg.estimate_utm_crs()

# restucture rainfall data to be long
# stack() by default dropna=True
df = (
    df_.set_index([c for c in df_.columns if c[0].isalpha()])
    .stack(dropna=True)
    .reset_index()
    .rename(columns={"level_5": "Date", 0: "Rainfall (mm)"})
    .drop(columns=["Station", "Longitude", "Latitude", "Elevation"])
)

df_stations = df_.loc[:, [c for c in df_.columns if c[0].isalpha()]]

# define function for performance testing...
def station_polys(how="boxes", step=200):
    if how == "voronoi":
        # generate a voronoi for all weather station points, clipped to Singapore boundary
        gdf_v = gpd.GeoDataFrame(
            geometry=[
                p.intersection(sg)
                for p in shapely.ops.voronoi_diagram(
                    shapely.geometry.MultiPoint(
                        gpd.points_from_xy(
                            df_stations["Longitude"], df_stations["Latitude"]
                        ),
                    ),
                ).geoms
            ],
            crs=gdf_sg.crs,
        ).to_crs(utm)

    elif how == "boxes":
        # number of meters
        STEP = step
        a, b, c, d = gdf_sg.to_crs(utm).total_bounds

        # create a grid for Singapore
        gdf_grid = gpd.GeoDataFrame(
            geometry=[
                shapely.geometry.box(minx, miny, maxx, maxy)
                for minx, maxx in zip(np.arange(a, c, STEP), np.arange(a, c, STEP)[1:])
                for miny, maxy in zip(np.arange(b, d, STEP), np.arange(b, d, STEP)[1:])
            ],
            crs=gdf_sg.estimate_utm_crs(),
        )
        gdf_v = gdf_grid.sjoin(gdf_sg.to_crs(utm)).drop(columns=["index_right", "name"])

    # associate voronoi or grid polygons with correct attributes (id)
    gdf_stations = (
        gpd.sjoin_nearest(
            gdf_v,
            gpd.GeoDataFrame(
                df_stations,
                geometry=gpd.points_from_xy(
                    df_stations["Longitude"], df_stations["Latitude"]
                ),
                crs=gdf_sg.crs,
            ).to_crs(utm),
        )
        .drop(columns=["index_right"])
        .dissolve("id")
    )
    return gdf_stations


gdf_stations = station_polys(how="voronoi", step=200)

# now associate geometry by station with rainfall data
gdf_rainfall = gpd.GeoDataFrame(pd.merge(df, gdf_stations, on="id"), crs=utm)

# let's plot what we have for a random date that has more stations in operation...
sample_date = np.random.choice(
    df.groupby("Date")["Rainfall (mm)"].sum().sort_values().index[-30:],
    1,
)[0]

sg_gridded_snapshot = gdf_rainfall.loc[lambda d: d["Date"].eq('20211231')].explore(
    column="Rainfall (mm)",
    missing_kwds={
        "color": "lightgrey",
    },
    height=400,
    width=700,
)

output_file = "map_Thiessen.html"
sg_gridded_snapshot.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab