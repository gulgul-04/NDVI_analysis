import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# Mask NDVI values within a specified date range for interpolation
def mask_dates_for_interpolation(dates, ndvi, start_str, end_str):
    dates_pd = pd.to_datetime(dates)
    start = pd.to_datetime(start_str)
    end = pd.to_datetime(end_str)
    ndvi_masked = np.array(ndvi, dtype=float)
    mask = (dates_pd >= start) & (dates_pd <= end)
    ndvi_masked[mask] = np.nan
    return ndvi_masked

#  fill missing NDVI values using spline interpolation
def spline_interpolate_ndvi(dates, ndvi):
    x = np.arange(len(dates))
    y = np.array(ndvi, dtype=float)
    mask = ~np.isnan(y)
    if mask.sum() < 2:
        # Not enough points to interpolate
        return y
    f_spline = interp1d(x[mask], y[mask], kind='cubic', fill_value='extrapolate')
    y_interp = f_spline(x)
    return y_interp
