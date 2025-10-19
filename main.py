"""
main.py
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
import os, zipfile

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

def main(folder, band_a_name, band_b_name, resolution, visualise, output):
    """
    Main function initiates functions to locate bands, compute NDI, display and save output.

    Parameters:
        folder (str): Root folder of Sentinel-2 data
        band_a_name (str): Band A identifier (e.g. B04)
        band_b_name (str): Band B identifier (e.g. B08)
        resolution (str): Spatial resolution (e.g. 10m)
        output (str): Output file path for NDI GeoTIFF
    """
    extracted_path=Path('Extracted')
    extracted_path.parent.mkdir(parents=True, exist_ok=True)

    for file in os.listdir(folder):
        if file.endswith(".zip"):
            filepath = Path(folder) / file
            zip = zipfile.ZipFile(filepath)
            zip.extractall(extracted_path)

    # Set up for Sentinel-2 file naming convention
    a_file = f'*{band_a_name}_{resolution}.jp2'
    b_file = f'*{band_b_name}_{resolution}.jp2'

    for safe_file in os.listdir(extracted_path):
        if safe_file.endswith(".SAFE"):
            safe_file = Path(extracted_path) / safe_file
            # Search recursively for red and NIR band files
            path_a = list(safe_file.rglob(a_file))
            path_b = list(safe_file.rglob(b_file))

            ndi = get_normalised_difference(path_a[0], path_b[0])

            # visualise the normalised difference
            if  visualise or __name__ == "__main__":
                plotting.plot_nd(ndi)

            # save to tif
            scene_name = safe_file.stem

            output_path = Path(output) / f"{scene_name}_{band_a_name}_{band_b_name}.tif"
            utils.write_geotiff(path_a[0], ndi, output_path)

if __name__=="__main__":
    cmdline = cli.cmd_arguments()
    folderpath = cmdline.folder
    band_a = cmdline.band_a
    band_b = cmdline.band_b
    resolution = cmdline.resolution
    visualise = cmdline.visualise
    output = cmdline.output
    main(folderpath, band_a, band_b, resolution, visualise, output)
