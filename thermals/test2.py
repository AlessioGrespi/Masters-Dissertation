import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')


def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image


# Load the image
image_path = 'render-4.png'
image = cv2.imread(image_path)

# Invert the image
image = invert_image(image)

# Define the kernel

kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

""" kernel = (1 / 3) * np.array([[0, 0, -1, 0, 0],
                   [0, -1, -2, -1, 0],
                   [-1, -2, 18.5, -2, -1],
                   [0, -1, -2, -1, 0],
                   [0, 0, -1, 0, 0]]) """

ridge_kernel = np.array([
                         [-1, 0, 1],
                         [-4, 0, 4],
                         [-1, 0, 1]
                         ])

blurred_kernel = (1 / 256) * np.array([[1, 4, 6, 4, 1],
                                       [4, 16, 24, 16, 4],
                                       [6, 24, 36, 24, 6],
                                       [4, 16, 24, 16, 4],
                                       [1, 4, 6, 6, 1]])

# Apply the convolution
output3 = cv2.filter2D(image, -1, kernel)
output3 = cv2.filter2D(output3, -1, kernel)
output3 = cv2.filter2D(output3, -1, kernel)
ridge_out = cv2.filter2D(output3, -1, ridge_kernel)
""" ridge_out = cv2.filter2D(output3, -1, ridge_kernel)
ridge_out = cv2.filter2D(output3, -1, ridge_kernel) """

# Convert images to RGB format
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
output3_rgb = cv2.cvtColor(output3, cv2.COLOR_BGR2RGB)
ridge_out_rgb = cv2.cvtColor(ridge_out, cv2.COLOR_BGR2RGB)

# Modify color channels for 'Sharpened' and 'Ridge' images
# Set green and blue channels to 0 (black and red color)
output3_rgb[:, :, 1:] = 0
# Set green and blue channels to 0 (black and red color)
ridge_out_rgb[:, :, 1:] = 0 

# Create a side-by-side plot
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
images = [image_rgb, output3, ridge_out]
titles = ['Original Image', 'Sharpened', 'Ridge']

for i in range(len(axes)):
    axes[i].imshow(images[i])
    axes[i].set_title(titles[i])
    axes[i].axis('off')

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0.03)

# Display the plot
plt.show()
