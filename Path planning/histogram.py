import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_ray_histogram(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate ray-level histogram
    histogram = np.zeros(256)
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            pixel_value = int(gray[i, j])
            histogram[pixel_value] += 1

    return histogram

def plot_ray_histogram(histogram):
    # Plotting the histogram
    plt.figure()
    plt.plot(histogram, color='black')
    plt.title("Ray-Level Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

def stretch_histogram(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Stretch the histogram using cv2.normalize()
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the normalized image back to the original color space
    stretched = cv2.cvtColor(normalized.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    return stretched

# Load the input image
input_path = "output_image.png"
input_image = cv2.imread(input_path)

# Calculate and plot ray-level histogram of the input image
input_histogram = calculate_ray_histogram(input_image)
plot_ray_histogram(input_histogram)

# Stretch the histogram of the input image
stretched_image = stretch_histogram(input_image)

# Display the input and stretched images side by side
combined_image = np.concatenate((input_image, stretched_image), axis=1)
cv2.imshow("Input Image vs. Stretched Image", combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
