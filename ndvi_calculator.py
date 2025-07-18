"""
Computes Normalised Difference Index from a Sentinel-2 Image
Inputs:
    - JP2 bands (e.g. B04 = red, B08 = NIR)
Outputs:
    - NDI as GeoTIFF
    - Optional NDI plot
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
        description="Run to calculate Normalised Difference Index from Sentinel-2 Image"
        )
    parser.add_argument(
        "--folder",
        dest="folder",
        type=str,
        default="Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE",
        help="Path to folder."
    )
    parser.add_argument(
        "--band-a",
        dest="band_a",
        type=str,
        default="B04",
        help="name of first band in normalised difference calculation"
    )
    parser.add_argument(
        "--band-b",
        dest="band_b",
        type=str,
        default="B08",
        help="name of second band in normalised difference calculation"
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
        default="Outputs/ndi.tif",
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

def calculate_normalised_difference(band_a, band_b):
    """
    Computes a Normalised Difference Index (NDI) from two input bands.

    Parameters:
        band_a (ndarray): First input band (e.g., red)
        band_b (ndarray): Second input band (e.g., NIR)

    Returns:
        ndi (ndarray): Array containing normalised difference values
    """
    # Convert to float for safe division
    band_a = band_a.astype(float)
    band_b = band_b.astype(float)

    # Calculate denominator and handle divide-by-zero
    denominator = band_b + band_a
    with np.errstate(divide='ignore', invalid='ignore'):
        ndi = (band_b - band_a) / denominator
        ndi[denominator == 0] = np.nan

    return ndi

def plot_nd(nd):
    # Displays as a red to green colour map
    plt.imshow(nd, cmap='RdYlGn')
    plt.colorbar(label='Normalised Difference Index')
    plt.title('Normalised Difference Index from Sentinel-2')
    plt.show()

def write_geotiff(src_path, ndi_array, output):
    """
    Creates geotiff of the ndi array

    Parameters:
        src_path(string or Path): path to a band to extract metadata
        ndi_array(array): results from normalised difference calculation
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
        dst.write(ndi_array.astype(rasterio.float32), 1)
        logger.info("GeoTIFF written to %s", output_path)

def get_normalised_difference(a_path, b_path):
    """
    Reads red and NIR band files and computes the NDI.

    Parameters:
        a_path (str or Path): Path to first band file
        b_path (str or Path): Path to second band file

    Returns:
        ndi (ndarray): NDI array
    """
    logging.info("Reading Band A: %s", a_path)
    a_band = read_file(a_path)
    logging.info("Reading Band B: %s",    b_path)
    b_band = read_file(b_path)

    nd = calculate_normalised_difference(a_band, b_band)

    logging.info("NDI calculation complete.")

    return nd

def main(folder, band_a_name, band_b_name, resolution, output):
    """
    Main function initiates functions to locate bands, compute NDI, display and save output.

    Parameters:
        folder (str): Root folder of Sentinel-2 data
        band_a_name (str): Band A identifier (e.g. B04)
        band_b_name (str): Band B identifier (e.g. B08)
        resolution (str): Spatial resolution (e.g. 10m)
        output (str): Output file path for NDI GeoTIFF
    """
    path = Path(folder)
    # Set up for Sentinel-2 file naming convention
    a_file = f'*{band_a_name}_{resolution}.jp2'
    b_file = f'*{band_b_name}_{resolution}.jp2'
    # Search recursively for red and NIR band files
    path_a = list(path.rglob(a_file))
    path_b = list(path.rglob(b_file))

    ndi = get_normalised_difference(path_a[0], path_b[0])

    plot_nd(ndi)

    write_geotiff(path_a[0], ndi, output)

if __name__=="__main__":
    cmdline = cmd_arguments()
    folderpath = cmdline.folder
    band_a = cmdline.band_a
    band_b = cmdline.band_b
    resolution = cmdline.resolution
    output = cmdline.output
    main(folderpath, band_a, band_b, resolution, output)