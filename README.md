# 🛰️ Sentinel-2 Normalised Difference Calculator

 This tool is for calculating **Normalized Difference Indices** (NDI) — like NDVI, NDWI, NBR — from Sentinel-2 `.jp2` band files. Useful for environmental monitoring and analysis.

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
 '''bash
 python main.py \
  --folder "Image/S2B_20250531T..." \
  --band-a B04 \
  --band-b B08 \
  --resolution 10m \
  --output Outputs/ndi.tif
  '''

 ## Roadmap
 [ ] Add optional geotiff and visualisation output<br>
 [ ] Add support for batch processing<br>
 [ ] Add support for cloud masking<br>
 [ ] Add progress bar for large files<br>
 [ ] Add test suite with pytest<br>

 ## Licence
 [MIT](https://choosealicense.com/licenses/mit/)

