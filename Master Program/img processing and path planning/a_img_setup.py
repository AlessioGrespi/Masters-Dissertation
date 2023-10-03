"""
IMG PREPREOCESSING FILE, HANDLES IMG SPLITTING AND GRAYSCALING. 

FILE IS COMPLETE AS OF 21/8/23 DO NOT MODIFY FURTHER
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import e_kernels as k
from PIL import Image

def convert_to_grayscale(input_image_path, output_image_path):
    try:
        # Open the image file
        with Image.open(input_image_path) as img:
            # Convert the image to grayscale
            grayscale_img = img.convert("L")
            
            # Save the grayscale image
            grayscale_img.save(output_image_path)
            print("Image converted to grayscale and saved")
    except Exception as e:
        print(f"Error: {e}")

def invert_image(image, output):

    image_map = cv2.imread(image)
    inverse = cv2.bitwise_not(image_map)

    cv2.imwrite(output, inverse)

    print("Image inverted and saved")
    return output

def img_split(image, threshold, output):
        # Load the image
    image_path = image
    image = cv2.imread(image_path)

    image_map = np.where(image > threshold, 255, 0).astype(np.uint8)

    cv2.imwrite(output, image_map)

    print("Image split and saved")

    return output

def setup_image(image_source, threshold, direction):
    convert_to_grayscale(image_source, "grayscale_map.png")

    img_split(image_source, threshold, "split_image_inverse.png")

    invert_image("split_image_inverse.png", "split_image.png")