import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan
import img_processing_and_path_planning.e_kernels as k
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

import csv

image_source = "render-7.png"
threshold = 256
map_translation = 0

# Example usage
start = (25, 25)
goal = (450, 450)

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create two empty lists to store the paths for different score weights
paths_score_2 = []
paths_score_4 = []
paths_score_6 = []
paths_score_8 = []

number_of_paths_distance = 8
score_weights = [2, 4, 6, 8]

image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'

direction = 230

for score_weight in score_weights:
    for i in range(number_of_paths_distance):
        weight = (i*2)+2
        
        map_creation(image_source, threshold, direction)
        
        # Call path_plan_stack and store the result in the appropriate list
        if score_weight == 2:
            path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
            paths_score_2.append(path_result)
        elif score_weight == 4:
            path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
            paths_score_4.append(path_result)
        elif score_weight == 6:
            path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
            paths_score_6.append(path_result)
        elif score_weight == 8:
            path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
            paths_score_8.append(path_result)

# Save paths to CSV
def save_paths_to_csv(paths, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Weight', 'Path'])
        for i, path in enumerate(paths):
            writer.writerow([i, path])

# Save paths for each score weight to CSV
save_paths_to_csv(paths_score_2, 'paths_score_2.csv')
save_paths_to_csv(paths_score_4, 'paths_score_4.csv')
save_paths_to_csv(paths_score_6, 'paths_score_6.csv')
save_paths_to_csv(paths_score_8, 'paths_score_8.csv')


# Load the source image
source_image = Image.open("split_image_inverse.png")

# Load the score map image using PIL
score_map_image = Image.open(score_map_path)

# Convert the score map image to a NumPy array
score_map_data = np.array(score_map_image)

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# Function to plot paths for a specific score weight
def plot_paths(ax, paths, weight):
    ax.imshow(source_image, cmap='gray')
    ax.imshow(score_map_data, alpha=1, cmap='gist_gray')
    ax.scatter(start[1], start[0], color='green', marker='o', label='Start')
    ax.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')
    for i, path in enumerate(paths):
        if path:
            path_y, path_x = zip(*path[0])
            ax.plot(path_x, path_y, label=f'Distance Weight {(i*2)+2}')
    

# Plot paths for score_weight 2
plot_paths(axs[0, 0], paths_score_2, 2)
axs[0, 0].legend(loc='upper right')
axs[0, 0].set_title(f'Score Weight: 2, Heading: {direction}')

# Plot paths for score_weight 4
plot_paths(axs[0, 1], paths_score_4, 4)
axs[0, 1].set_title(f'Score Weight: 4, Heading: {direction}')
axs[0, 1].legend(loc='lower left')

# Plot paths for score_weight 6
plot_paths(axs[1, 0], paths_score_6, 6)
axs[1, 0].set_title(f'Score Weight: 6, Heading: {direction}')
axs[1, 0].legend(loc='lower left')

# Plot paths for score_weight 8
plot_paths(axs[1, 1], paths_score_8, 8)
axs[1, 1].set_title(f'Score Weight: 8, Heading: {direction}')
axs[1, 1].legend(loc='lower left')

plt.tight_layout()
plt.show()
