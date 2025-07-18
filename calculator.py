import numpy as np

def normalised_difference(band_a, band_b):
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