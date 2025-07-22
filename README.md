# 🛰️ Sentinel-2 Normalised Difference Calculator

 A Python module for calculating **Normalized Difference Indices** (NDI) — like NDVI, NDWI, NBR — from Sentinel-2 `.jp2` band files. Outputs a GeoTIFF and plot.

 ## Features
 - Reads Sentinel-2 .jp2 band data
 - Calculates NDI: (B - A) / (B + A)
 - Outputs a Geotiff
 - Displays a plot
 - Command-line interface

 ## Requirements
 - Python 3.8+
 - rasterio, numpy, argparse, matplotlib

 ## Installation
 

 ## Usage
 
 Example
 python main.py \
  --folder "Image/S2B_20250531T..." \
  --band-a B04 \
  --band-b B08 \
  --resolution 10m \
  --output Outputs/ndi.tif

 ## Roadmap
 [ ] Add optional geotiff and visualisation output<br>
 [ ] Add support for batch processing<br>
 [ ] Add support for cloud masking<br>
 [ ] Add progress bar for large files<br>
 [ ] Add test suite with pytest<br>

 ## Licence

