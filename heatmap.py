import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image

# Load your grayscale PNG image
image_path = 'trimmed_map.png'
grayscale_image = np.array(Image.open(image_path).convert('L'))  # Convert to grayscale

# Normalize the grayscale image to the range [0, 1]
grayscale_image = grayscale_image / 255.0

# Choose a colormap (colormaps represent the "heat" levels)
colormap = 'summer'  # You can choose from various colormaps like 'hot', 'cool', 'jet', etc.

# Create a colormap instance
cmap = plt.get_cmap(colormap)

# Create a heatmap by applying the colormap to the grayscale image
heatmap = cmap(grayscale_image)

# Display the heatmap
plt.imshow(heatmap, cmap=colormap)
plt.axis('off')  # Remove axes if needed

# Save or display the heatmap
plt.savefig('heatmap.png')  # Save as an image
plt.show()  # Display the heatmap in a window

# To save the heatmap as an image with a color bar, you can use the following code:
# fig, ax = plt.subplots()
# im = ax.imshow(heatmap, cmap=colormap)
# cbar = plt.colorbar(im)
# plt.savefig('heatmap_with_colorbar.png')
# plt.show()
