import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

# Load the image
image_path = 'render-2.png'
image = cv2.imread(image_path)

# Invert the image
inverted_image = invert_image(image)

# Define the kernel
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

# Apply the convolution
output1 = cv2.filter2D(inverted_image, -1, kernel)
output2 = cv2.filter2D(output1, -1, kernel)
output3 = cv2.filter2D(output2, -1, kernel)

# Create a side-by-side plot
fig, axes = plt.subplots(1, 4, figsize=(16, 5))
images = [inverted_image, output1, output2, output3]
titles = ['Original Image', 'Convolved 1', 'Convolved 2', 'Convolved 3']

for i in range(len(axes)):
    axes[i].imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    axes[i].set_title(titles[i])
    axes[i].axis('off')

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0.03)

# Display the plot
plt.show()
