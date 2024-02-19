"""
IMG FILTER FILE, HANDLES THE APPLICATION OF VARIOUS FILTERS 
TO HIGHLIGHT SLOPES AND RIDGE AREAS

FILE IS COMPLETE AS OF 21/8/23 DO NOT MODIFY FURTHER
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

def ridge_filter(image, direction):


    direction_rad = math.radians(direction)

    
    if (0 <= direction <= 90):
        weighting = math.sin(direction_rad) # 0 -> 1
        S2N_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))
        W2E_kernel = 0.5 * (k.W2E_kernel * weighting)

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
            # Clip the pixel values to ensure they are within the specified range
        #S2N_image = np.clip(S2N_image, 0, 255)
        #W2E_image = np.clip(W2E_image, 0, 255)

        output = S2N_image + W2E_image

        #output = np.clip(output, 0, 255)

    if (90 < direction <= 180):
        weighting = math.sin(direction_rad) # 1 -> 0
        
        W2E_kernel = 0.5 * (k.W2E_kernel * weighting)
        N2S_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
        output = N2S_image + W2E_image

    if (180 < direction <= 270):
        weighting = -(math.sin(direction_rad)) # 0 -> 1
        
        E2W_kernel = 0.5 * (k.E2W_kernel * weighting)
        N2S_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = N2S_image + E2W_image
    if (270 < direction <= 360):
        weighting = -(math.sin(direction_rad)) # 1 -> 0
        
        E2W_kernel = 0.5 * (k.E2W_kernel * weighting)
        S2N_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = S2N_image + E2W_image
   


    """ 
    direction_rad = math.radians(direction)

    if (0 <= direction <= 90):
        weighting = math.sin(direction_rad) # 0 -> 1
        S2N_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))
        W2E_kernel = 0.5 * (k.E2W_kernel * weighting)

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
            # Clip the pixel values to ensure they are within the specified range
        #S2N_image = np.clip(S2N_image, 0, 255)
        #W2E_image = np.clip(W2E_image, 0, 255)

        output = S2N_image + W2E_image

        #output = np.clip(output, 0, 255)

    if (90 < direction <= 180):
        weighting = math.sin(direction_rad) # 1 -> 0
        
        W2E_kernel = 0.5 * (k.E2W_kernel * weighting)
        N2S_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
        output = N2S_image + W2E_image

    if (180 < direction <= 270):
        weighting = -(math.sin(direction_rad)) # 0 -> 1
        
        E2W_kernel = 0.5 * (k.W2E_kernel * weighting)
        N2S_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = N2S_image + E2W_image
    if (270 < direction <= 360):
        weighting = -(math.sin(direction_rad)) # 1 -> 0
        
        E2W_kernel = 0.5 * (k.W2E_kernel * weighting)
        S2N_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = S2N_image + E2W_image
     """
    #print("Weighting: ", weighting)
  

    #output = cv2.filter2D(image, -1, ridge_kernel)
    return output

def sharpen_less_filter(image):
    kernel2 = np.array([
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]])

    output = cv2.filter2D(image, -1, kernel2)
    return output

def blur_filter(image):
    output = cv2.filter2D(image, -1, k.blurred_kernel)
    return output

def normalisation_filter(image):
    output = cv2.filter2D(image, -1, k.normalisation_kernel)
    return output


def apply_ridge_filters(path_to_img, direction, output_file, map_translation):
    
    """ # Load the image
    image_path = path_to_img
    image = cv2.imread(image_path)

    output = image

    #cv2.imwrite("img_step_1.png", output)
    #output = sharpen_filter(output)
    #cv2.imwrite("img_step_2.png", output)
    output = ridge_filter(output, direction)
    #cv2.imwrite("img_step_3.png", output)
    #output = ridge_filter(output, direction)
    #cv2.imwrite("img_step_4.png", output)
    #output = sharpen_less_filter(output)
    #cv2.imwrite("img_step_5.png", output)
    #output = blur_filter(output)
    #cv2.imwrite("img_step_6.png", output)


    output = normalisation_filter(output)
    #output = normalisation_filter(output) 
    #output = sobel_y(output)
    
    # Threshold the image
    threshold = 1
    output[output > threshold] += map_translation

    # Set blue and green channels to zero
    output[:, :, 0] = 0
    output[:, :, 1] = 0

    # Move the ridge lift output to the red channel
    red_channel = output[:, :, 2]

    # Create a blank image with only the red channel
    red_image = np.zeros_like(image)
    red_image[:, :, 2] = red_channel

    # Save the final image
    final_image_path = output_file
    cv2.imwrite(final_image_path, red_image) """

    

    """ #print("Image filters applied and saved")


     # Load the image
    image_path = path_to_img
    image = cv2.imread(image_path)

    output = image

    # Comment out the previous filtering steps and keep the ridge filter only
    #output = sharpen_filter(output)
    output = ridge_filter(output, direction)
    #output = ridge_filter(output, direction)
    #output = sharpen_less_filter(output)
    #output = blur_filter(output)
    #output = np.where(output < 5, 0, output)
    # Convert the output to grayscale
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    #output = np.where(output > 255, 255, output)
    
    output = cv2.bitwise_not(output)  # Invert the image
 




    threshold = 250
     """

    image_path = path_to_img
    image = cv2.imread(image_path)

    output = image
    output = sharpen_filter(output)
    cv2.imwrite("sharpened_image.png", output)
    #output = normalisation_filter(output)

    #output = sharpen_filter(output)
    output = ridge_filter(output, direction)
    cv2.imwrite("ridged_image.png", output)
    #output = normalisation_filter(output)


    # Convert the output to grayscale
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    # Invert the image first
    #output = cv2.bitwise_not(output)

    # Threshold the image
    threshold = 0
    output[output > threshold] += map_translation
    cv2.imwrite("ridged_image.png", output)
    # Save the grayscale image
    cv2.imwrite(output_file, output)

    print("Image filters applied and saved")





""" 
def grayscale_ridge_lift(path_to_img, direction):
    # Load the image
    image_path = path_to_img
    image = cv2.imread(image_path)

    output = image

    output = sharpen_filter(output)
    output = ridge_filter(output, direction)
    output = ridge_filter(output, direction)
    output = sharpen_less_filter(output)
    output = blur_filter(output)

    # Convert the output to grayscale
    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    # Save the final grayscale image
    final_image_path = 'Grayscale_Ridge_Lift_Output.png'
    cv2.imwrite(final_image_path, gray_output)

def overlay_grayscale_ridge(ridge_lift_path, split_image_path, output_path):
    # Load the grayscale ridge lift output image
    grayscale_ridge_img = cv2.imread(ridge_lift_path, cv2.IMREAD_GRAYSCALE)

    # Load the split image
    split_img = cv2.imread(split_image_path)

    # Create a blank image with the same dimensions as the split image
    overlay_img = np.zeros_like(split_img)

    # Assign the grayscale ridge lift output to the overlay image
    overlay_img[:, :, 0] = grayscale_ridge_img

    # Add the overlay image to the split image
    result = cv2.addWeighted(split_img, 1, overlay_img, 1, 0)

    output = invert_image(result)
    # Save the result to a separate file
    cv2.imwrite(output_path, output) """

""" ridge_lift_path = "Ridge_Lift_Output.png"
split_image_path = "Split_Image.png"
output_path = "Map+Ridge.png"
output_path_grayscale = "Map+GrayscaleRidge.png" """

#ridge_lift("render-5.png", 90)
#grayscale_ridge_lift("render-5.png", 90)
#img_split("render-5.png", 70)





#### ridge filter for demo map, not real map
""" 

def ridge_filter(image, direction):


    direction_rad = math.radians(direction)

    if (0 <= direction <= 90):
        weighting = math.sin(direction_rad) # 0 -> 1
        S2N_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))
        W2E_kernel = 0.5 * (k.W2E_kernel * weighting)

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
            # Clip the pixel values to ensure they are within the specified range
        #S2N_image = np.clip(S2N_image, 0, 255)
        #W2E_image = np.clip(W2E_image, 0, 255)

        output = S2N_image + W2E_image

        #output = np.clip(output, 0, 255)

    if (90 < direction <= 180):
        weighting = math.sin(direction_rad) # 1 -> 0
        
        W2E_kernel = 0.5 * (k.W2E_kernel * weighting)
        N2S_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        W2E_image = cv2.filter2D(image, -1, W2E_kernel)
        output = N2S_image + W2E_image

    if (180 < direction <= 270):
        weighting = -(math.sin(direction_rad)) # 0 -> 1
        
        E2W_kernel = 0.5 * (k.E2W_kernel * weighting)
        N2S_kernel = 0.5 * (k.N2S_kernel * (1 - weighting))

        N2S_image = cv2.filter2D(image, -1, N2S_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = N2S_image + E2W_image
    if (270 < direction <= 360):
        weighting = -(math.sin(direction_rad)) # 1 -> 0
        
        E2W_kernel = 0.5 * (k.E2W_kernel * weighting)
        S2N_kernel = 0.5 * (k.S2N_kernel * (1 - weighting))

        S2N_image = cv2.filter2D(image, -1, S2N_kernel)
        E2W_image = cv2.filter2D(image, -1, E2W_kernel)
        output = S2N_image + E2W_image
     """