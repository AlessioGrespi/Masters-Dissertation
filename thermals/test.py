import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def apply_convolution(image, kernel):
    # Convert the image and kernel to numpy arrays
    image_array = np.array(image)
    kernel_array = np.array(kernel)
    
    # Normalize the kernel to ensure proper convolution
    kernel_array = kernel_array / np.sum(kernel_array)
    
    # Apply the convolution to each color channel
    output_array = np.zeros_like(image_array)
    for channel in range(image_array.shape[2]):
        output_array[:, :, channel] = convolve2d(image_array[:, :, channel], kernel_array, mode='same', boundary='symm')
    
    # Clip the output values to ensure they are within valid image range
    output_array = np.clip(output_array, 0, 255)
    
    # Convert the output array back to uint8 and return as image
    output_image = output_array.astype(np.uint8)
    
    return output_image

# Load the image
image_path = 'render-2.png'  # Replace with the actual path to your image
image = mpimg.imread(image_path)

# Define the convolutional kernel
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# Apply the convolution
output_image = apply_convolution(image, kernel)

# Display the original and convolved images
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(output_image)
plt.title('Convolved Image')

# Print the range of values in the output array
print('Output array range:', np.min(output_image), np.max(output_image))

plt.show()
