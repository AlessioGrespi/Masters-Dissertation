import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.patches import Polygon

def import_image(file_path):
    image = Image.open(file_path).convert("L")  # Convert image to grayscale
    print("Importing the image")
    return np.array(image)

def split_image(image, threshold):
    gray_image = image.copy()
    gray_image[gray_image <= threshold] = 0  # Pixels below or equal to threshold are set to black
    gray_image[gray_image > threshold] = 255  # Pixels above threshold are set to white
    obstacles = []
    i = 0
    print("Splitting the image")
    for row in range(image.shape[0] - 1):
        for col in range(image.shape[1] - 1):
            i += 1
            print("progress: ", i / ((image.shape[0] - 1)*(image.shape[1] - 1)), "%")
            if gray_image[row, col] == 255:
                obstacle = Polygon([(col, image.shape[0] - 1 - row), (col + 1, image.shape[0] - 1 - row),
                                    (col + 1, image.shape[0] - 1 - row - 1), (col, image.shape[0] - 1 - row - 1)])
                obstacles.append(obstacle)
    return obstacles

file_path = "render-4.png"
threshold = 70
image = import_image(file_path)
obstacles = split_image(image, threshold)

# Plot the obstacle polygons
print("plotting obstacles")
for obstacle in obstacles:
    print(obstacle, "of", obstacles)
    plt.plot(*obstacle.exterior.xy, 'r-')

# Display the plot
plt.show()
