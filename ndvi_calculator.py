import rasterio
import matplotlib.pyplot as plt
from pathlib import Path

def read_file(filepath):
    with rasterio.open(filepath) as src:
        return src.read(1)

def calculate_ndvi(red, nir):
    ndvi = (nir.astype(float) - red.astype(float))/(nir.astype(float) + red.astype(float))
    return ndvi

def plot_ndvi(ndvi):
    plt.imshow(ndvi, cmap='BuGn')
    plt.colorbar(label='NDVI')
    plt.title('NDVI from Sentinel-2')
    plt.show()

def main():
    redfile = read_file(Path('Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\GRANULE\L2A_T60HWC_A043012_20250531T220639\IMG_DATA\R10m\T60HWC_20250531T220619_B04_10m.jp2'))

    nirfile = read_file(Path('Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\GRANULE\L2A_T60HWC_A043012_20250531T220639\IMG_DATA\R10m\T60HWC_20250531T220619_B08_10m.jp2'))

    ndvi = calculate_ndvi(redfile, nirfile)

    plot_ndvi(ndvi)

if __name__=="__main__":
    main()