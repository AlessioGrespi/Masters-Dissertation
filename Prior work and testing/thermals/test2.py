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

kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]])

kernel2 = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]])

""" ridge_kernel = np.array([
    [-1, -1, 0, 1, 1],
    [-1, -2, 0, 2, 1],
    [-1, -4, 0, 4, 1],
    [-1, -2, 0, 2, 1],
    [-1, -1, 0, 1, 1]
]) """

ridge_kernel = np.array([
    [-1, -1, -1, -1, -1],
    [-1, -2, -4, -2, -1],
    [0, 0, 0, 0, 0],
    [1, 2, 4, 2, 1],
    [1, 1, 1, 1, 1]
])

y_kernel = np.array([
    [0.33,0.33,0.33],
    [-0.67,-0.67,-0.67],
    [0,0,0]
])

blurred_kernel = (1 / 256) * np.array([[1, 4, 6, 4, 1],
                                       [4, 16, 24, 16, 4],
                                       [6, 24, 36, 24, 6],
                                       [4, 16, 24, 16, 4],
                                       [1, 4, 6, 6, 1]])

# Apply the convolution
output3 = cv2.filter2D(image, -1, kernel)
#output3 = cv2.filter2D(output3, -1, kernel)
#output3 = cv2.filter2D(output3, -1, kernel)
ridge_out = cv2.filter2D(output3, -1, ridge_kernel)
ridge_out = cv2.filter2D(ridge_out, -1, ridge_kernel)
ridge_out = cv2.filter2D(ridge_out, -1, kernel2)
ridge_out = cv2.filter2D(ridge_out, -1, blurred_kernel)
#ridge_out = cv2.filter2D(ridge_out, -1, y_kernel)

# Save the final image
final_image_path = 'final_image.png'
cv2.imwrite(final_image_path, ridge_out)

# Display the plot
#plt.show()
