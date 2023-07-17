
import cv2
import numpy as np
import matplotlib.pyplot as plt

def invert_image(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

def sharpen_filter(image):
    
    kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]])

    output = cv2.filter2D(image, -1, kernel)
    return output

def ridge_filter(image, direction):
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

    output = cv2.filter2D(image, -1, ridge_kernel)
    return output

def sharpen_less_filter(image):
    kernel2 = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]])

    output = cv2.filter2D(image, -1, kernel2)
    return output

def blur_filter(image):
    blurred_kernel = (1 / 256) * np.array([[1, 4, 6, 4, 1],
                                       [4, 16, 24, 16, 4],
                                       [6, 24, 36, 24, 6],
                                       [4, 16, 24, 16, 4],
                                       [1, 4, 6, 6, 1]])
    
    output = cv2.filter2D(image, -1, blurred_kernel)
    return output

def sobel_y(image):
    sobel_y = np.array([
                        [3, 10, 3],
                        [0, 0, 0],
                        [-1, -5, -1],
                        [-1, -5, -1],
                        [-1, -5, -1],
                        [-1, -5, -1],
                        ])
    
    output = cv2.filter2D(image, -1, sobel_y)
    return output

def ridge_lift(path_to_img, direction):
    
    # Load the image
    image_path = path_to_img
    image = cv2.imread(image_path)

    # Invert the image
    output = invert_image(image)

    output = sharpen_filter(output)
    output = ridge_filter(output, direction)
    output = ridge_filter(output, direction)
    output = sharpen_less_filter(output)
    output = blur_filter(output)
    #output = sobel_y(output)

    # Set blue and green channels to zero
    output[:, :, 0] = 0
    output[:, :, 1] = 0

    # Move the ridge lift output to the red channel
    red_channel = output[:, :, 2]

    # Create a blank image with only the red channel
    red_image = np.zeros_like(image)
    red_image[:, :, 2] = red_channel

    # Save the final image
    final_image_path = 'Ridge_Lift_Output.png'
    cv2.imwrite(final_image_path, red_image)

def img_split(path_to_img, threshold):
        # Load the image
    image_path = path_to_img
    image = cv2.imread(image_path)

    image_map = np.where(image > threshold, 255, 0).astype(np.uint8)

    cv2.imwrite("Split_Image.png", image_map)



def overlay_red_channel(ridge_lift_path, split_image_path, output_path):
    # Load the ridge lift output image
    ridge_lift_img = cv2.imread(ridge_lift_path)

    # Load the split image
    split_img = cv2.imread(split_image_path)

    # Extract the red channel from the ridge lift output
    red_channel = ridge_lift_img[:, :, 2]

    # Create a blank image with the same dimensions as the split image
    overlay_img = np.zeros_like(split_img)

    # Assign the red channel to the overlay image
    overlay_img[:, :, 2] = red_channel

    # Add the overlay image to the split image
    result = cv2.addWeighted(split_img, 1, overlay_img, 1, 0)

    output = invert_image(result)
    # Save the result to a separate file
    cv2.imwrite(output_path, output)

ridge_lift_path = "Ridge_Lift_Output.png"
split_image_path = "Split_Image.png"
output_path = "Map+Ridge.png"

ridge_lift("render-4.png", 0)
img_split("render-4.png", 70)

overlay_red_channel(ridge_lift_path, split_image_path, output_path)