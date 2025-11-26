import numpy as np
import ee
from tqdm import tqdm
from datetime import datetime, timezone

def extract_ndvi_stats(image_list, region, count):
    # Prepare lists to hold statistics
    dates = []
    means = []
    medians = []
    stds = []
    perc_10 = []
    perc_90 = []
    valid_pixels = []
    total_pixels = []

    # Iterate through each image to compute statistics and accumulate results
    for i in tqdm(range(count), desc="Processing NDVI stats"):
        img = ee.Image(image_list.get(i))

        # Calculate NDVI statistics for valid (unmasked) pixels
        stats = img.select('NDVI').clip(region).reduceRegion(
            reducer=ee.Reducer.median()
                .combine(ee.Reducer.mean(), '', True)
                .combine(ee.Reducer.stdDev(), '', True)
                .combine(ee.Reducer.percentile([10, 90]), '', True)
                .combine(ee.Reducer.count(), '', True),
            geometry=region,
            scale=10,
            maxPixels=int(1e9)
        )
        mean   = stats.get('NDVI_mean').getInfo()
        median = stats.get('NDVI_median').getInfo()
        std    = stats.get('NDVI_stdDev').getInfo()
        p10    = stats.get('NDVI_p10').getInfo()
        p90    = stats.get('NDVI_p90').getInfo()
        count_valid = stats.get('NDVI_count').getInfo()

        # Calculate total number of pixels in region (no masking)
        total_stats = ee.Image.constant(1).clip(region).reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=region,
            scale=10,
            maxPixels=int(1e9)
        )
        count_total = total_stats.get('constant').getInfo()

        # Extract timestamp for date
        tstamp = img.get('system:time_start').getInfo()
        date_str = datetime.fromtimestamp(tstamp/1000, tz=timezone.utc).strftime('%Y-%m-%d') if tstamp else "Unknown"

        dates.append(date_str)
        means.append(mean)
        medians.append(median)
        stds.append(std)
        perc_10.append(p10)
        perc_90.append(p90)
        valid_pixels.append(count_valid)
        total_pixels.append(count_total)

    # Clean and align arrays
    ndvi_data = [
        (d, mn, md, sd, p1, p9, vp, tp)
        for d, mn, md, sd, p1, p9, vp, tp in zip(dates, means, medians, stds, perc_10, perc_90, valid_pixels, total_pixels)
        if (mn is not None and md is not None and sd is not None and p1 is not None and p9 is not None and vp is not None and tp is not None)
    ]

    if ndvi_data:
        dates_f, means_f, medians_f, stds_f, perc_10_f, perc_90_f, pixels_f, total_pixels_f = zip(*ndvi_data)
        means_f        = np.array(means_f, dtype=float)
        medians_f      = np.array(medians_f, dtype=float)
        stds_f         = np.array(stds_f, dtype=float)            
        perc_10_f      = np.array(perc_10_f, dtype=float)
        perc_90_f      = np.array(perc_90_f, dtype=float)
        pixels_f       = np.array(pixels_f, dtype=int)
        total_pixels_f = np.array(total_pixels_f, dtype=int)
        return (dates_f, means_f, medians_f, stds_f, perc_10_f, perc_90_f, pixels_f, total_pixels_f)
    else:
        return [], np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
