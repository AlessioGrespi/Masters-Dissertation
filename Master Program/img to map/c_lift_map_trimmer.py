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
    _, binary_mask = cv2.threshold(two_tone, 1, 255, cv2.THRESH_BINARY)

    # Set the pixels in the grayscale image to zero where the mask is black
    result = cv2.bitwise_and(grayscale, cv2.bitwise_not(binary_mask))

    return result

def trim_reward_map(grayscale_image_path, two_tone_image_path, output):
    # Paths to your grayscale and two-tone images
    grayscale_image_path = "ridge_map.png"
    two_tone_image_path = "split_image_inverse.png"

    # Apply the mask and get the result
    result_image = apply_two_tone_mask(grayscale_image_path, two_tone_image_path)
    print("Lift map trimmed and saved")
    cv2.imwrite(output, result_image)
    a_img_setup.invert_image(output, output)