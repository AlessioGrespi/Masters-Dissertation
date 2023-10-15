import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'trimmed_map.png'  # Replace with your image file path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Could not open or read the image.")
    exit()

# Calculate the histogram
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

# Flatten the histogram into a 1-D array
hist = hist.flatten()

# Create a histogram plot
plt.figure(figsize=(10, 5))
plt.title("Gray-Level Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.xlim([0, 256])  # Set the x-axis limits to 0-255
plt.plot(hist, color='gray')
plt.grid()
plt.show()
