import matplotlib.pyplot as plt

def plot_nd(nd):
    # Displays as a red to green colour map
    plt.imshow(nd, cmap='RdYlGn')
    plt.colorbar(label='Normalised Difference Index')
    plt.title('Normalised Difference Index from Sentinel-2')
    plt.show()
