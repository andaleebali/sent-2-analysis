# plotting.py
import matplotlib.pyplot as plt
import numpy as np
def plot_nd(nd):
    # Displays as a red to green colour map
    plt.imshow(nd, cmap='RdYlGn')
    plt.colorbar(label='Normalised Difference Index')
    plt.title('Normalised Difference Index from Sentinel-2')
    plt.show()

def plot_histogram(ndi_array):
    data = ndi_array[~np.isnan(ndi_array)]
    plt.figure(figsize=(8,5))
    plt.hist(data, bins=50, edgecolor='black')
    plt.show()
    