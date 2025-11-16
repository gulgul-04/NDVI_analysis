import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

# NDVI stage definitions for single crop cycle (mutually exclusive)
def get_stage_colors(ndvi):
    ndvi = np.array(ndvi)
    ndvi_diff = np.diff(ndvi, prepend=ndvi[0])
    colors = []
    for i, val in enumerate(ndvi):
        if val < 0.1:
            colors.append("#b3c6e0")    # empty field/water (light blue)
        elif 0.1 <= val < 0.3:
            colors.append("#cccccc")    # bare/low cover (gray)
        elif 0.3 <= val < 0.75 and ndvi_diff[i] >= 0:
            colors.append("#3ac96a")    # rapid growth (bright green)
        elif 0.75 <= val <= 1.0:
            colors.append("#005902")    # peak (dark green)
        elif 0.3 < val < 0.75 and ndvi_diff[i] < 0:
            colors.append("#f5c542")    # senescence/maturity (yellow)
        else:
            colors.append("#cccccc")    # fallback: bare/low
    return colors


# Plotting functions for NDVI statistics
# plotting mean NDVI with stage-aware shading
def plot_mean_ndvi(dates_f, means_f, means_gauss):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    plt.plot(dates_f, means_f, label="Raw Mean NDVI", marker='o')
    plt.plot(dates_f, means_gauss, label="Smoothed Mean NDVI", color="orange", linewidth=2)
    # Stage-aware shading
    stages = get_stage_colors(means_gauss)
    for i in range(1, len(dates_f)):
        ax.fill_between(dates_f[i-1:i+1], 0, means_gauss[i-1:i+1], color=stages[i], alpha=0.38)
    plt.legend()
    plt.grid(True)
    plt.title("Mean NDVI (Growth Stages Highlighted)")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Mean NDVI")
    plt.tight_layout()
    plt.show()

# plotting median NDVI with stage-aware shading
def plot_median_ndvi(dates_f, medians_f, medians_gauss):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    plt.plot(dates_f, medians_f, label="Raw Median NDVI", marker='o', color="green")
    plt.plot(dates_f, medians_gauss, label="Smoothed Median NDVI", color="blue", linewidth=2)
    stages = get_stage_colors(medians_gauss)
    for i in range(1, len(dates_f)):
        ax.fill_between(dates_f[i-1:i+1], 0, medians_gauss[i-1:i+1], color=stages[i], alpha=0.38)
    plt.title("Median NDVI Over Time (Growth Stages Highlighted)")
    plt.xlabel("Date")
    plt.ylabel("Median NDVI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plotting NDVI standard deviation
def plot_ndvi_stddev(dates_f, stds_f, stds_gauss):
    plt.figure(figsize=(12,6))
    plt.plot(dates_f, stds_f, label="Raw NDVI StdDev", marker='o', color="red")
    plt.plot(dates_f, stds_gauss, label="Smoothed NDVI StdDev", color="orange", linewidth=2)
    plt.title("NDVI Standard Deviation Over Time")
    plt.xlabel("Date")
    plt.ylabel("StdDev NDVI")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plotting NDVI percentiles
def plot_ndvi_percentiles(dates_f, perc_10_f, p10_gauss, perc_90_f, p90_gauss):
    plt.figure(figsize=(12,6))
    plt.plot(dates_f, perc_10_f, label="Raw NDVI 10th Percentile", marker='o', color="purple")
    plt.plot(dates_f, p10_gauss, label="Smoothed 10th Percentile", color="magenta", linewidth=2)
    plt.plot(dates_f, perc_90_f, label="Raw NDVI 90th Percentile", marker='o', color="orange")
    plt.plot(dates_f, p90_gauss, label="Smoothed 90th Percentile", color="darkorange", linewidth=2)
    plt.title("NDVI Percentiles Over Time")
    plt.xlabel("Date")
    plt.ylabel("NDVI Value")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plotting valid pixel count
def plot_valid_pixel_count(dates_f, pixels_f):
    plt.figure(figsize=(12,6))
    plt.plot(dates_f, pixels_f, label="Valid Pixels", marker='o', color="blue")
    plt.title("Valid NDVI Pixel Count Over Time")
    plt.xlabel("Date")
    plt.ylabel("Pixel Count")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plotting all NDVI statistics together
def plot_all_ndvi_statistics(dates_f, means_gauss, medians_gauss, p10_gauss, p90_gauss, stds_gauss):
    plt.figure(figsize=(16,8))
    plt.plot(dates_f, means_gauss, label="Mean NDVI (Smoothed)", marker='o')
    plt.plot(dates_f, medians_gauss, label="Median NDVI (Smoothed)", marker='o')
    plt.plot(dates_f, p10_gauss, label="10th Percentile (Smoothed)", linestyle="--")
    plt.plot(dates_f, p90_gauss, label="90th Percentile (Smoothed)", linestyle="--")
    plt.plot(dates_f, stds_gauss, label="StdDev (Smoothed)", linestyle=":", color="red")
    plt.title("All NDVI Statistics (Smoothed)")
    plt.xlabel("Date")
    plt.ylabel("NDVI value")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plotting mean NDVI with spline interpolation
def plot_mean_ndvi_with_spline(dates_f, means_f, means_spline, means_gauss):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    plt.plot(dates_f, means_f, label="Raw Mean NDVI", marker='o', color="blue")
    plt.plot(dates_f, means_gauss, label="Smoothed Mean NDVI", color="orange", linewidth=2)
    plt.plot(dates_f, means_spline, label="Spline Interpolated NDVI", color="magenta", linestyle="--", linewidth=2)
    stages = get_stage_colors(means_gauss)
    for i in range(1, len(dates_f)):
        ax.fill_between(dates_f[i-1:i+1], 0, means_gauss[i-1:i+1], color=stages[i], alpha=0.38)
    plt.legend()
    plt.grid(True)
    plt.title("Mean NDVI (Raw, Smoothed, Spline Interpolated)")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Mean NDVI")
    plt.tight_layout()
    plt.show()

#plotting mean ndvi with linear interpolation
def plot_mean_ndvi_with_linear(dates_f, means_f, means_linear, means_gauss):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    plt.plot(dates_f, means_f, label="Raw Mean NDVI", marker='o', color="blue")
    plt.plot(dates_f, means_gauss, label="Smoothed Mean NDVI", color="orange", linewidth=2)
    plt.plot(dates_f, means_linear, label="Linear Interpolated NDVI", color="green", linestyle=":", linewidth=2)
    stages = get_stage_colors(means_gauss)
    for i in range(1, len(dates_f)):
        ax.fill_between(dates_f[i-1:i+1], 0, means_gauss[i-1:i+1], color=stages[i], alpha=0.38)
    plt.legend()
    plt.grid(True)
    plt.title("Mean NDVI (Raw, Smoothed, Linear Interpolated)")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Mean NDVI")
    plt.tight_layout()
    plt.show()