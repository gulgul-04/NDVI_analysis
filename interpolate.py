import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator, UnivariateSpline

# Mask NDVI values within a specified date range for interpolation
def mask_dates_for_interpolation(dates, ndvi, start_str, end_str, outside_to_nan=False):
    dates_pd = pd.to_datetime(dates)
    start = pd.to_datetime(start_str)
    end = pd.to_datetime(end_str)

    ndvi_masked = np.asarray(ndvi, dtype=float).copy()

    # Core mask: inside the period that should be interpolated
    in_window = (dates_pd >= start) & (dates_pd <= end)

    if outside_to_nan:
        # Optional: keep only this window, drop outside
        mask = ~in_window
        ndvi_masked[mask] = np.nan
    else:
        # Default: only blank out this window, keep the rest unchanged
        ndvi_masked[in_window] = np.nan

    return ndvi_masked

#  fill missing NDVI values using spline interpolation
def spline_interpolate_ndvi(dates, ndvi, method='pchip', smooth=None):
     # Convert dates (possibly strings) to np.datetime64 or pd.Timestamp
    if isinstance(dates[0], str):
        dates = np.array(pd.to_datetime(dates))
    else:
        dates = np.array(dates)
        if not np.issubdtype(dates.dtype, np.datetime64):
            dates = np.array(pd.to_datetime(dates))

    # Now subtraction works:
    x_full = (dates - dates[0]).astype("timedelta64[D]").astype(float)

   # Convert dates to numeric (days since first date)
    dates = np.asarray(dates)
    y = np.asarray(ndvi, dtype=float)

    # Handle all-NaN or single-point case
    mask = ~np.isnan(y)
    if mask.sum() < 2:
        return y

    # Use real time axis
    x_full = (dates - dates[0]).astype("timedelta64[D]").astype(float)
    x = x_full[mask]
    y_valid = y[mask]

    if method == "pchip":
        # Shape-preserving, monotone, safer for NDVI
        f = PchipInterpolator(x, y_valid, extrapolate=False)
        y_interp = f(x_full)
    elif method == "cubic":
        # Similar to your original, but on real time axis and no extrapolation
        from scipy.interpolate import interp1d
        f = interp1d(x, y_valid, kind="cubic",
                     bounds_error=False, fill_value="extrapolate")
        y_interp = f(x_full)
    elif method == "univariate":
        # Smoothing spline, good if NDVI is noisy
        if smooth is None:
            # heuristic: small smoothing factor
            smooth = len(x) * 1e-3
        f = UnivariateSpline(x, y_valid, s=smooth)
        y_interp = f(x_full)
    else:
        raise ValueError("method must be 'pchip', 'cubic', or 'univariate'")
    
    # Optionally, keep NaNs outside the observed date range
    x_min, x_max = x.min(), x.max()
    outside = (x_full < x_min) | (x_full > x_max)
    y_interp[outside] = np.nan

    return y_interp