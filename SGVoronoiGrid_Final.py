# get data from csv
import pandas as pd
df_ = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vS2ijDtnQnbjVhKO1n-9QcIWz2DTPIAxZ7GcIKzNdxEDlxDD6HOO0kITMBDv0sXOTuvLVDnBhx34DIv/pub?gid=186097297&single=true&output=csv")

import shapely.geometry, shapely.ops
import geopandas as gpd
import numpy as np
import webbrowser

gdf_sg = gpd.read_file(
    "https://raw.githubusercontent.com/yinshanyang/singapore/master/maps/0-country.geojson"
)
# Singapore boundary as a shapely multipolygon
sg = gdf_sg.dissolve()["geometry"].values[0]
utm = gdf_sg.estimate_utm_crs()

# restucture rainfall data to be long
# stack() by default dropna=True
df = (
    df_.set_index([c for c in df_.columns if c[0].isalpha()])
    .stack(dropna=False)
    .reset_index()
    .rename(columns={"level_5": "Date", 0: "Rainfall (mm)"})
    .drop(columns=["Station", "Longitude", "Latitude", "Elevation"])
)

df_stations = df_.loc[:, [c for c in df_.columns if c[0].isalpha()]]

# make a grid of boxes covering Singapore
def make_grid(step=500):
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
    return gdf_grid.sjoin(gdf_sg.to_crs(utm)).drop(columns=["index_right", "name"])


# define function for performance testing...
def station_polys(how="boxes", gdf_grid=None, ids=df_stations["id"].tolist()):
    df_stations_ = df_stations.merge(pd.Series(ids, name="id"), on="id")
    if how == "voronoi":
        # generate a voronoi for all weather station points, clipped to Singapore boundary
        gdf_v = gpd.GeoDataFrame(
            geometry=[
                p.intersection(sg)
                for p in shapely.ops.voronoi_diagram(
                    shapely.geometry.MultiPoint(
                        gpd.points_from_xy(
                            df_stations_["Longitude"], df_stations_["Latitude"]
                        ),
                    ),
                ).geoms
            ],
            crs=gdf_sg.crs,
        ).to_crs(utm)

    elif how == "boxes":
        gdf_v = gdf_grid

    # associate voronoi or grid polygons with correct attributes (id)
    gdf_stations = (
        gpd.sjoin_nearest(
            gdf_v,
            gpd.GeoDataFrame(
                df_stations_,
                geometry=gpd.points_from_xy(
                    df_stations_["Longitude"], df_stations_["Latitude"]
                ),
                crs=gdf_sg.crs,
            ).to_crs(utm),
        )
        .drop(columns=["index_right"])
        .dissolve("id")
    )
    return gdf_stations

def polys_for_combis(head=5, how="voronoi", gdf_grid=None):
    # have to be tuples so they are immutable and hashable for join
    # association between Date and combination of station ids
    s_combi = (
        df.dropna()
        .sort_values(["Date", "id"])
        .groupby("Date")["id"]
        .agg(tuple)
        .rename("combi")
    )

    # unique combinations, plus give them an id
    df_combi = pd.DataFrame({"combi": np.unique(s_combi)}).assign(
        combi_id=lambda d: d.index
    )
    # for testing use subset of combinations
    if head is not None:
        df_combi = df_combi.sample(n=head, random_state=44)

    # construct geometry for each combination of stations
    gdf_combi = pd.concat(
        [
            station_polys(how=how, ids=combi, gdf_grid=gdf_grid)
            .reset_index()
            .assign(combi_id=combi_id)
            for combi_id, combi in df_combi.set_index("combi_id")["combi"].iteritems()
        ]
    )

    # add date for combi and join in rainfall data
    gdf_rainfall = gdf_combi.merge(
        df_combi.merge(s_combi.reset_index(), on="combi").drop(columns=["combi"]),
        on="combi_id",
    ).merge(df, on=["id", "Date"])

    return gdf_rainfall

#gdf_stations = station_polys(how="voronoi")
gdf_grid = make_grid(step=200)
gdf_stations = station_polys(how="boxes", gdf_grid=gdf_grid)

# now associate geometry by station with rainfall data
gdf_rainfall = gpd.GeoDataFrame(pd.merge(df, gdf_stations, on="id"), crs=utm)

sample_date = "19801020" # staged, many NaNs and significant rainfall
plot_opts = dict(
    column="Rainfall (mm)",
    missing_kwds={
        "color": "lightgrey",
    },
    height=300,
    width=500,
)

m_nan = gdf_rainfall.loc[lambda d: d["Date"].eq(sample_date)].explore(**plot_opts)

gdf_grid = make_grid(step=200)
gdf_rainfall = polys_for_combis(how="boxes", gdf_grid=gdf_grid)
#gdf_rainfall = polys_for_combis(how="voronoi", head=None)
m_no_nan = gdf_rainfall.loc[lambda d: d["Date"].eq(sample_date)].explore(**plot_opts)

'''
# visualize map with folium
output_file = "map_voronoi_grid.html"
m_no_nan.save(output_file)
webbrowser.open(output_file, new=2)  # open in new tab
'''

print(gdf_rainfall)