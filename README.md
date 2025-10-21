# 🛰️ Sentinel-2 Normalised Difference Calculator

 This tool is for calculating **Normalized Difference Indices** (NDI) — like NDVI, NDWI, NBR — from Sentinel-2 `.jp2` band files. Useful for environmental monitoring and analysis.

 ## Features
 - Reads Sentinel-2 .jp2 band data
 - Calculates NDI: (B - A) / (B + A)
 - Outputs a Geotiff
 - Displays a plot
 - Optional Visualisation
 - Command-line interface

 ## Requirements
 - Python 3.8+
 - Packages: rasterio, numpy, argparse, matplotlib

 Install them with:
    ```bash
    pip install -r requirements.txt
    ```

 ## Installation
 1. Clone this repository
 ```bash
 git clone https://github.com/andaleebali/sent-2-analysis.git 
 cd sent-2-analysis
 ```
 2. Create a virtual environment (optional)
 ```bash
 python -m venv venv 
 source venv/bin/activate # or on Windows: venv\Scripts\activate
 ```
 3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
 ## Usage
 
 Example
 ```bash
 python main.py \
  --folder "Inputs" \
  --band-a B04 \
  --band-b B08 \
  --resolution 10m \
  --output Outputs/
  ```

  Example 
  ```bash
  
  ```
 ## Output

 ## Roadmap
 [ ] Add optional geotiff and visualisation output<br>
 [ ] Add support for batch processing<br>
 [ ] Add support for cloud masking<br>
 [ ] Add progress bar for large files<br>
 [ ] Add unit tests (pytest)<br>

 ## Licence
 [MIT](https://choosealicense.com/licenses/mit/)

