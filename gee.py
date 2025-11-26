import ee
from pyproj import Transformer
from cloud_mask import mask_clouds_s2

def initialize_ee(project=None):
    if project:
        ee.Initialize(project=project)
    else:
        ee.Initialize()
    print("Google Earth Engine initialized successfully.")


def transform_coords(coords_meters, from_crs="EPSG:3857", to_crs="EPSG:4326"):
    transformer = Transformer.from_crs(from_crs, to_crs)
    coords_lonlat = [transformer.transform(x, y) for x, y in coords_meters]
    # pyproj returns (lat, lon), swap to (lon, lat)
    coords_lonlat_fixed = [[lon, lat] for lat, lon in coords_lonlat]
    # Close the polygon
    if coords_lonlat_fixed[0] != coords_lonlat_fixed[-1]:
        coords_lonlat_fixed.append(coords_lonlat_fixed[0])
    return coords_lonlat_fixed

def create_region(coords_lonlat):
    region = ee.Geometry.Polygon(coords_lonlat)
    return region

def load_s2_collection(region, start_date, end_date, cloud_pct=30):
    ic = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_pct))
        .filterBounds(region)
    )
    return ic

'''def mask_clouds_s2(img):
    qa = img.select('QA60')
    cloudBitMask  = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
        qa.bitwiseAnd(cirrusBitMask).eq(0))
    return img.updateMask(mask)'''

def add_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

def mask_and_calculate_ndvi(ic, cloud_threshold=30):
    ic_masked = ic.map(lambda img: mask_clouds_s2(img, cloud_threshold))
    ndvi_collection = ic_masked.map(add_ndvi)
    return ndvi_collection