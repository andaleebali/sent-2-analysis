import rasterio
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import numpy as np
import argparse
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cmdLine():
    p = argparse.ArgumentParser(
        description="Run to calculate NDVI from Sentinel-2 Image"
        )
    
    p.add_argument(
        "--folder",
        dest="folder",
        type=str,
        default="Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE",
        help="Path to folder and name."
    )
    cmd = p.parse_args()
    return cmd

def read_file(filepath):
    with rasterio.open(filepath) as src:
        return src.read(1)

def calculate_ndvi(red, nir):
    nir = nir.astype(float)
    red = red.astype(float)

    denominator = nir + red
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir - red)/denominator
        ndvi[denominator==0] = np.nan
        
    return ndvi

def plot_ndvi(ndvi):
    plt.imshow(ndvi, cmap='BuGn')
    plt.colorbar(label='NDVI')
    plt.title('NDVI from Sentinel-2')
    plt.show()

def main(folder):

    path = Path(folder)
    redpath = list(path.rglob('R10m/*B04_10m.jp2'))
    nirpath = list(path.rglob('R10m/*B08_10m.jp2'))

    logging.info("Reading red band %s.", redpath)
    red_band = read_file(redpath[0])

    logging.info("Reading NIR band %s.",    nirpath)
    nir_band = read_file(nirpath[0])

    ndvi = calculate_ndvi(red_band, nir_band)

    logging.info("NDVI calculation complete.")

    plot_ndvi(ndvi)

if __name__=="__main__":
    cmdline = cmdLine()
    folderpath = cmdline.folder
    main(folderpath)