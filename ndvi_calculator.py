import rasterio
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    redfile = Path('Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\GRANULE\L2A_T60HWC_A043012_20250531T220639\IMG_DATA\R10m\T60HWC_20250531T220619_B04_10m.jp2')

    nirfile = Path('Image\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\S2B_MSIL2A_20250531T220619_N0511_R086_T60HWC_20250531T233234.SAFE\GRANULE\L2A_T60HWC_A043012_20250531T220639\IMG_DATA\R10m\T60HWC_20250531T220619_B08_10m.jp2')
    
    with rasterio.open(redfile) as red:
        red = red.read(1)

    with rasterio.open(nirfile) as nir:
        nir = nir.read(1)

    ndvi = (nir.astype(float) - red.astype(float))/(nir.astype(float) + red.astype(float))

    print(ndvi)

    plt.imshow(ndvi, cmap='BuGn')
    plt.colorbar(label='NDVI')
    plt.title('NDVI from Sentinel-2')
    plt.show()

if __name__=="__main__":
    main()