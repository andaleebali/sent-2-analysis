# Command line arguments

import argparse

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
        default="Inputs",
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
        help="set resolution"
    )

    parser.add_argument(
        "--visualise",
        action="store_true",
        help="show result once calculated"
    )

    parser.add_argument(
        "--output",
        dest="output",
        default="Outputs",
        help="folder name for outputs"
    )

    cmd = parser.parse_args()
    return cmd