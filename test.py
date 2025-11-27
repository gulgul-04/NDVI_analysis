# test.py
import ee
import gee
from cloud_mask import mask_clouds_s2
import stats

# 1. Basic initialization and collection info
def test_init_and_collection(region_coords_meters):
    print("=== Test 1: EE init & collection ===")
    gee.initialize_ee(project='brijesh-ndvi')
    coords_lonlat_fixed = gee.transform_coords(region_coords_meters)
    region = gee.create_region(coords_lonlat_fixed)

    ic = gee.load_s2_collection(region, '2023-12-01', '2024-12-01', cloud_pct=90)
    count = ic.size().getInfo()
    print(f"Image count in raw collection: {count}")

    first_img = ee.Image(ic.first())
    print("Bands in first image:", first_img.bandNames().getInfo())
    return ic, region


# 2. Check QA60 cloud mask effect on a single image
def test_cloud_mask_effect(ic, region, cloud_threshold=30):
    print("\n=== Test 2: QA60 / CLDPRB mask effect ===")
    first_img = ee.Image(ic.first())

    qa0 = first_img.select('QA60')
    total0 = qa0.reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=10,
        maxPixels=1e9
    ).get('QA60').getInfo()

    masked0 = mask_clouds_s2(first_img, cloud_threshold)
    qa0_masked = masked0.select('QA60')
    valid0 = qa0_masked.reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=10,
        maxPixels=1e9
    ).get('QA60').getInfo()

    print(f"QA60 pixels before mask: {total0}, after mask: {valid0}")
    if total0:
        print(f"Fraction kept (first image): {valid0/total0:.4f}")
    else:
        print("No QA60 pixels in region.")


# 3. Check NDVI mask & valid vs total pixels across several images
def test_ndvi_valid_fraction(ic, region, cloud_threshold=30, max_images=5):
    print("\n=== Test 3: NDVI valid vs total pixels ===")
    ndvi_collection = gee.mask_and_calculate_ndvi(ic, cloud_threshold=cloud_threshold)
    count = ndvi_collection.size().getInfo()
    print(f"NDVI collection size: {count}")

    use_count = min(count, max_images)
    image_list = ndvi_collection.toList(use_count)

    dates_f, means_f, medians_f, stds_f, p10_f, p90_f, pixels_f = stats.extract_ndvi_stats(image_list, region, use_count, show_progress=False)

    for i in range(len(dates_f)):
        vp = pixels_f[i]
        print(f"{i:02d} Date {dates_f[i]}: valid={vp}")


# 4. Master runner
def run_all_tests():
    # Same coords as in main.py
    coords_meters = [
        [8915601.024032443761826, 3231775.347342940047383],
        [8915666.145934557542205, 3231874.193312517367303],
        [8915875.98317470215261,  3231767.792266437318176],
        [8915823.291206929832697, 3231663.280803931877017],
    ]

    ic, region = test_init_and_collection(coords_meters)
    test_cloud_mask_effect(ic, region, cloud_threshold=30)
    test_ndvi_valid_fraction(ic, region, cloud_threshold=30, max_images=5)


if __name__ == "__main__":
    run_all_tests()
