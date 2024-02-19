import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan
import img_processing_and_path_planning.e_kernels as k
import matplotlib.pyplot as plt  # Importing the correct module for plotting
from PIL import Image
import numpy as np

image_source = "render-7.png"
threshold = 256
map_translation = 0
direction= 90

# Example usage
start = (25, 25)
goal = (450, 450)

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create an empty list to store the paths
paths = []

number_of_paths = 10

weight = 1  # distance weight



# Load the score map image using PIL
score_map_path = 'trimmed_map.png'
score_map_image = Image.open(score_map_path)

image_path = 'split_image.png'

# Load the source image
source_image = Image.open(image_source)
# Convert the score map image to a NumPy array
score_map_data = np.array(score_map_image)

# Create a single matplotlib window with subplots for each path
plt.figure(figsize=(15, 10))

for i in range(number_of_paths):
    score_weight = i
    
    map_creation(image_source, threshold, direction)
    
    # Call path_plan_stack and store the result in the paths list
    path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
    paths.append(path_result)

    # Create a subplot for each path
    plt.subplot(3, 4, i + 1)  # Adjust the number of rows and columns as needed
    plt.imshow(source_image, cmap='gray')
    plt.imshow(score_map_data, alpha=1, cmap='gist_gray')  # Ensure 'cmap' is set to 'hot'
    plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
    plt.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')
    
    if path_result:
        path_y, path_x = zip(*path_result)
        plt.plot(path_x, path_y, label=f'Score Weight {i * 2}')
    
    plt.legend()
    # plt.title(f'A* Pathfinding with Score Map (Score Weight {i * 2})')

# Adjust the layout to ensure subplots don't overlap
plt.tight_layout()

plt.show()
