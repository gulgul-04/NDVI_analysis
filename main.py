from scipy.ndimage import gaussian_filter1d
import plot
import stats
import gee
import interpolate

#Define the region of interest 
coords_meters = [
    [ 8915601.024032443761826, 3231775.347342940047383 ], 
    [ 8915666.145934557542205, 3231874.193312517367303 ], 
    [ 8915875.98317470215261, 3231767.792266437318176 ], 
    [ 8915823.291206929832697, 3231663.280803931877017 ]
]  

# Initialize GEE and load image collection
print("Initializing Earth Engine...")
gee.initialize_ee(project='brijesh-ndvi')

#Define region and transform coordinates
print("Transforming coordinates and creating region...")
coords_lonlat_fixed = gee.transform_coords(coords_meters)
region = gee.create_region(coords_lonlat_fixed)

# Load Sentinel-2 image collection
print("Loading Sentinel-2 collection...")
ic = gee.load_s2_collection(region, '2023-12-01', '2024-12-01', cloud_pct=90)

count_before = ic.size().getInfo()
print(f"Number of images in collection before masking: {count_before}")

# Masking and NDVI are done together in module
ndvi_collection = gee.mask_and_calculate_ndvi(ic, cloud_threshold=30)
ndvi_median = ndvi_collection.select('NDVI').median().clip(region)
count = ndvi_collection.size().getInfo()
print(f"Number of images in NDVI collection: {count}")

image_list = ndvi_collection.toList(count)

# Extract NDVI statistics
dates_f, means_f, medians_f, stds_f, perc_10_f, perc_90_f, pixels_f, fractions_f = stats.extract_ndvi_stats(image_list, region, count)

# Handle missing data with spline and linear interpolation
means_f_masked = interpolate.mask_dates_for_interpolation(
    dates_f, 
    means_f, 
    "2024-06-01", "2024-10-22",
    outside_to_nan=False
)
means_spline = interpolate.spline_interpolate_ndvi(
    dates_f, 
    means_f_masked,
    method="univariate",
    smooth=None    
)


# Gaussian smoothing (sigma=2 recommended; adjust for smoothness)
sigma = 2
means_gauss   = gaussian_filter1d(means_f, sigma=sigma)
medians_gauss = gaussian_filter1d(medians_f, sigma=sigma)
stds_gauss    = gaussian_filter1d(stds_f, sigma=sigma)
p10_gauss     = gaussian_filter1d(perc_10_f, sigma=sigma)
p90_gauss     = gaussian_filter1d(perc_90_f, sigma=sigma)

# Pretty text table (aligned)
header = "|   Date     |  Mean   | Median  |  Std    |  10%    |  90%    | Pixels  | Fraction |"
separator = "|------------|---------|---------|---------|---------|---------|---------|----------|"
print(header)
print(separator)

# Helper function for formatting
def fmt(val):
    return f"{val:7.4f}"

for d, mn, m, s, p1, p9, c, vf in zip(dates_f, means_f, medians_f, stds_f, perc_10_f, perc_90_f, pixels_f, fractions_f):
    print(f"| {d:<10} | {fmt(mn)} | {fmt(m)} | {fmt(s)} | {fmt(p1)} | {fmt(p9)} | {c:7d} | {fmt(vf)} |")


# Generate plots using the plot module
plot.plot_mean_ndvi(dates_f, means_f, means_gauss)
plot.plot_median_ndvi(dates_f, medians_f, medians_gauss)
plot.plot_ndvi_stddev(dates_f, stds_f, stds_gauss)
plot.plot_ndvi_percentiles(dates_f, perc_10_f, p10_gauss, perc_90_f, p90_gauss)
plot.plot_valid_pixel_count(dates_f, pixels_f)
plot.plot_valid_pixel_fraction(dates_f, fractions_f)
plot.plot_all_ndvi_statistics(dates_f, means_gauss, medians_gauss, p10_gauss, p90_gauss, stds_gauss)
plot.plot_mean_ndvi_with_spline(dates_f, means_f, means_spline, means_gauss)
