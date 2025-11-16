# NDVI Time Series Analysis

This repository provides code and tools for processing and analyzing NDVI time series data for crop phenology and remote sensing studies. It addresses gaps in satellite vegetation indices (due to clouds or missing data) by allowing you to mask periods and apply gap-filling techniques such as spline interpolation.

**Code Structure:**
- `main.py` — Orchestrates workflow
- `gee.py` — Google Earth Engine data utils
- `interpolate.py` — NDVI gap-filling methods
- `plot.py` — Visualization routines
- `stats.py` — Statistical analysis and summaries
- `gpkg_extract.py` — Extracts and processes GeoPackage data

**Features:**
- Modular code for easy maintenance and extension
- Masking and handling missing/cloudy data in time series
- Gap-filling with cubic spline or linear interpolation
- Generation of raw, smoothed, and interpolated NDVI plots
- Publication-ready figures for phenology and agri research

**Usage:**
1. Place your NDVI dataset in the project folder.
2. Configure date ranges and modules as needed.
3. Run scripts to process and visualize NDVI time series, comparing interpolation methods.

**Requirements:**
- Python 3.x
- numpy, pandas, matplotlib, scipy, ee, tqdm

**Applications:**  
Crop monitoring, remote sensing analytics, phenology research, gap-filling in EO time series.
