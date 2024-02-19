"""
IMG FILTER FILE, HANDLES THE APPLICATION OF VARIOUS FILTERS 
TO HIGHLIGHT SLOPES AND RIDGE AREAS

FILE IS COMPLETE AS OF 21/8/23 DO NOT MODIFY FURTHER
"""
""" 
""" 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import img_processing_and_path_planning.e_kernels as k

def sharpen_filter(image):
    
    kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def sobelx_filter(image):
    
    kernel = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def gaussian_filter(image):
    kernel = (1 / 256) * np.array([[1, 4, 6, 4, 1],
                                        [4, 16, 24, 16, 4],
                                        [6, 24, 36, 24, 6],
                                        [4, 16, 24, 16, 4],
                                        [1, 4, 6, 6, 1]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def sobely_filter(image):
    
    kernel = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def normal_filter(image):
    
    kernel = (1/9)*np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def blur_filter(image):
    output = cv2.filter2D(image, -1, k.blurred_kernel)
    return output

def normalisation_filter(image):
    output = cv2.filter2D(image, -1, k.normalisation_kernel)
    return output 


path_to_img = "DSC05165.jpg"
output_file = "normalise_image.jpg"

image_path = path_to_img
image = cv2.imread(image_path)

# Convert the image to grayscale
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply the Sobel y filter to the grayscale image
normal = normal_filter(image)

# Save the result
cv2.imwrite("image_normalised.png", normal)

blur = blur_filter(image)

cv2.imwrite("image_blurred.png", blur)

# sobel_x = sobelx_filter(image)

# cv2.imwrite("image_sobel_x.png", sobel_x)


# sobel_y = sobely_filter(image)

# cv2.imwrite("image_sobel_y.png", sobel_y)

sharp = sharpen_filter(image)

cv2.imwrite("image_sharpened.png", sharp)

gauss = gaussian_filter(image)

cv2.imwrite("image_gaussian.png",gauss)

print("Image filters applied and saved")

 
""" 
path_to_img = "DSC05165.jpg"
output_file = "sobel_combined_image.jpg"

image_path = path_to_img
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Calculate the Sobel X and Sobel Y gradients
sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# Calculate the gradient magnitude
gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

# Normalize the gradient magnitude image (optional)
gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Save the combined gradient magnitude image
cv2.imwrite(output_file, gradient_magnitude)
 """