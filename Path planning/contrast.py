import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance

def increase_contrast(image_path, output_path, contrast_factor):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to grayscale if it's not already
    image = image.convert("L")

    # Increase the contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)

    # Save the modified image
    image.save(output_path)

# Example usage
input_image_path = "render-4.png"
output_image_path = "output_image.png"
contrast_factor = 1.5  # Increase this value to increase contrast

increase_contrast(input_image_path, output_image_path, contrast_factor)

# Plot the images and histograms side by side
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
input_image = Image.open(input_image_path)
output_image = Image.open(output_image_path)

# Display input image
axes[0, 0].imshow(input_image, cmap='gray')
axes[0, 0].set_title('Input Image')

# Display input image histogram
axes[1, 0].hist(np.array(input_image).ravel(), bins=256, color='gray')
axes[1, 0].set_title('Input Image Histogram')

# Display modified image
axes[0, 1].imshow(output_image, cmap='gray')
axes[0, 1].set_title('Modified Image')

# Display modified image histogram
axes[1, 1].hist(np.array(output_image).ravel(), bins=256, color='gray')
axes[1, 1].set_title('Modified Image Histogram')

# Remove ticks
for ax in axes.flatten():
    ax.axis('off')

# Adjust spacing
plt.tight_layout()

# Show the plot
plt.show()
