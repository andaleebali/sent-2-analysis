import rasterio
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
