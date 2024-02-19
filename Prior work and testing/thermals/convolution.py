import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# Generate a random grid
grid = np.random.randint(0, 255, size=(20, 20), dtype=np.uint8)

# Define the smoothing kernel (Gaussian blur)
smoothing_kernel = np.array([[1, 2, 1],
                             [2, 4, 2],
                             [1, 2, 1]])

# Apply the smoothing kernel
smoothed = convolve(grid, smoothing_kernel, mode='constant', cval=0.0)

# Define the sharpening kernel
sharpening_kernel = np.array([[0, -1, 0],
                              [-1, 5, -1],
                              [0, -1, 0]])

# Apply the sharpening kernel
sharpened = convolve(smoothed, sharpening_kernel, mode='constant', cval=0.0)

# Define the edge detection kernel
edge_kernel = np.array([[-1, -1, -1],
                        [-1, 8, -1],
                        [-1, -1, -1]])

# Apply the edge detection kernel
edges = convolve(sharpened, edge_kernel, mode='constant', cval=0.0)

# Create a figure and subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Plot the original grid
axes[0, 0].imshow(grid, cmap='hot')
axes[0, 0].set_title("Original Grid")

# Plot the smoothed grid
axes[0, 1].imshow(smoothed, cmap='hot')
axes[0, 1].set_title("Smoothed Grid")

# Plot the sharpened grid
axes[1, 0].imshow(sharpened, cmap='hot')
axes[1, 0].set_title("Sharpened Grid")

# Plot the edges
axes[1, 1].imshow(edges, cmap='hot')
axes[1, 1].set_title("Edges")

# Adjust spacing and display the plot
plt.tight_layout()
plt.show()
