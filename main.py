"""
Computes Normalised Difference Index from a Sentinel-2 Image
Inputs:
    - JP2 bands (e.g. B04 = red, B08 = NIR)
Outputs:
    - NDI as GeoTIFF
    - Optional NDI plot
"""

import logging
from pathlib import Path
import cli
import calculator
import plotting
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    a_band = utils.read_file(a_path)
    logging.info("Reading Band B: %s",    b_path)
    b_band = utils.read_file(b_path)

    nd = calculator.normalised_difference(a_band, b_band)

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

    plotting.plot_nd(ndi)

    utils.write_geotiff(path_a[0], ndi, output)

if __name__=="__main__":
    cmdline = cli.cmd_arguments()
    folderpath = cmdline.folder
    band_a = cmdline.band_a
    band_b = cmdline.band_b
    resolution = cmdline.resolution
    output = cmdline.output
    main(folderpath, band_a, band_b, resolution, output)
