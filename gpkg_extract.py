import geopandas as gpd
import pandas as pd

data = gpd.read_file("131_farms.gpkg")
pd.set_option('display.max_rows', None)
print(data)

data.to_file("output.geojson", driver='GeoJSON')
