"""
TRIMS THE SCORE MAP TO ONLY SHOW AREAS WHICH ARE NAVIGABLE

FILE IS COMPLETE AS OF 25/8/23 DO NOT MODIFY FURTHER
"""

import cv2
import numpy as np
import a_img_setup

def apply_two_tone_mask(grayscale_image, two_tone_image):
    # Load the grayscale and two-tone images
    grayscale = cv2.imread(grayscale_image, cv2.IMREAD_GRAYSCALE)
    two_tone = cv2.imread(two_tone_image, cv2.IMREAD_GRAYSCALE)

    # Make sure the images are the same size
    if grayscale.shape != two_tone.shape:
        raise ValueError("Images must be the same size")

    # Convert the two-tone image to a binary mask
    _, binary_mask = cv2.threshold(two_tone, 0, 255, cv2.THRESH_BINARY)

    # Set the pixels in the grayscale image to zero where the mask is black
    result = cv2.bitwise_and(grayscale, cv2.bitwise_not(binary_mask))

    return result


from PIL import Image

def make_white_pixels_transparent(input_image_path, output_image_path):
    # Open the input image
    image = Image.open(input_image_path)

    # Convert the image to RGBA mode to handle transparency
    image = image.convert("RGBA")

    # Get the pixel data as a list of tuples
    pixel_data = list(image.getdata())

    # Iterate through all pixels and make completely white pixels transparent
    new_pixel_data = [(r, g, b, 0) if r == 255 and g == 255 and b == 255 else (r, g, b, a) for r, g, b, a in pixel_data]

    # Update the image with the modified pixel data
    image.putdata(new_pixel_data)

    # Save the resulting image
    image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "input.png"  # Replace with your input image path
    output_image_path = "output.png"  # Replace with the desired output image path
    make_white_pixels_transparent(input_image_path, output_image_path)


def trim_reward_map(grayscale_image_path, two_tone_image_path, output):
    # Paths to your grayscale and two-tone images
    grayscale_image_path = "ridge_map.png"
    two_tone_image_path = "split_image_inverse.png"

    # Apply the mask and get the result
    result_image = apply_two_tone_mask(grayscale_image_path, two_tone_image_path)
    print("Lift map trimmed and saved")
    cv2.imwrite(output, result_image)
    a_img_setup.invert_image(output, output)

    #make_white_pixels_transparent(output,output)

    