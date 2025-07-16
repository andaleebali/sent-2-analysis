"""
Compute NDVI from a Sentinel-2 Image
Inputs:
    - JP2 bands (e.g. B04 = red, B08 = NIR)
Outputs:
    - NDVI as GeoTIFF
    - Optional NDVI plot
"""

import logging
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import rasterio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cmd_arguments():
    """
    Parsers for the command line
    
    Returns:
        cmd: arguments

    """
    parser = argparse.ArgumentParser(
        description="Run to calculate NDVI from Sentinel-2 Image"
        )
    parser.add_argument(
        "--folder",
        dest="folder",
        type=str,
        default="Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE",
        help="Path to folder."
    )
    parser.add_argument(
        "--red-band",
        dest="redband",
        type=str,
        default="B04",
        help="name of red band"
    )
    parser.add_argument(
        "--nir-band",
        dest="nirband",
        type=str,
        default="B08",
        help="name of NIR band"
    )
    parser.add_argument(
        "--resolution",
        dest="resolution",
        type=str,
        default="10m",
        help="resolution"
    )
    parser.add_argument(
        "--output",
        dest="output",
        default="Outputs/ndvi.tif",
        help="file name for outputs"
    )

    cmd = parser.parse_args()
    return cmd

def read_file(filepath):
    """
    Reads a single band from a raster file and returns as an array.

    Parameters:
        filepath (string or Path): Full path to raster file.

    Returns:
        src (ndarray) 2D array of pixel values
    """
    with rasterio.open(filepath) as src:
        return src.read(1)

def calculate_ndvi(red, nir):
    """
    Computes NDVI from red and NIR bands.

    Parameters:
        red (ndarray): red band array
        nir (ndarray): NIR band array

    Returns:
        ndvi (ndarray): NDVI calculation result

    """
    # sets values to floats for correct division
    nir = nir.astype(float)
    red = red.astype(float)

    # calculates ndvi unless denominator is 0
    denominator = nir + red
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = (nir - red)/denominator
        #Sets value to NaN when denominator is 0
        ndvi[denominator==0] = np.nan
    return ndvi

def plot_ndvi(ndvi):
    # Displays as a red to green colour map
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar(label='NDVI')
    plt.title('NDVI from Sentinel-2')
    plt.show()

def write_geotiff(src_path, ndvi, output):
    """
    Creates geotiff of the ndvi array

    Parameters:
        src_path(string or Path): path to a band to extract metadata
        ndvi(array): results from normalised difference calculation
        output(string): location to save output
    """
    # Checks output folder exists 
    output_path=Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy metadata from source image
    with rasterio.open(src_path) as file:
        kwargs = file.meta
        kwargs.update(
        dtype=rasterio.float32,
        count=1,
        nodata = np.nan,
        driver='GTiff')

    with rasterio.open(output_path,'w',**kwargs) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)
        logger.info("GeoTIFF written to %s", output_path)

def get_ndvi(redpath, nirpath):
    """
    Reads red and NIR band files and computes the NDVI.

    Parameters:
        redpath (str or Path): Path to red band file
        nirpath (str or Path): Path to NIR band file

    Returns:
        ndvi (ndarray): NDVI array
    """
    logging.info("Reading red band %s.", redpath)
    red_band = read_file(redpath)
    logging.info("Reading NIR band %s.",    nirpath)
    nir_band = read_file(nirpath)

    ndvi = calculate_ndvi(red_band, nir_band)

    logging.info("NDVI calculation complete.")

    return ndvi

def main(folder, redband, nirband, resolution, output):
    """
    Main function initiates functions to locate bands, compute NDVI, display and save output.

    Parameters:
        folder (str): Root folder of Sentinel-2 data
        redband (str): Red band identifier (e.g. B04)
        nirband (str): NIR band identifier (e.g. B08)
        resolution (str): Spatial resolution (e.g. 10m)
        output (str): Output file path for NDVI GeoTIFF
    """
    path = Path(folder)
    # Set up for Sentinel-2 file naming convention
    red_file = f'*{redband}_{resolution}.jp2'
    nir_file = f'*{nirband}_{resolution}.jp2'
    # Search recursively for red and NIR band files
    redpath = list(path.rglob(red_file))
    nirpath = list(path.rglob(nir_file))

    ndvi = get_ndvi(redpath[0], nirpath[0])

    plot_ndvi(ndvi)

    write_geotiff(redpath[0], ndvi, output)

if __name__=="__main__":
    cmdline = cmd_arguments()
    folderpath = cmdline.folder
    redband = cmdline.redband
    nirband = cmdline.nirband
    resolution = cmdline.resolution
    output = cmdline.output
    main(folderpath, redband, nirband, resolution, output)