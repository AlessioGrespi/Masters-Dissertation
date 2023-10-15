import a_img_setup as setup
import b_filtering as filtering
import c_lift_map_trimmer as lift_trimmer
import d_pathplanning as pathplan
import matplotlib.pyplot as plt  # Importing the correct module for plotting
from PIL import Image

image_source = "render-7.png"
threshold = 256
map_translation = 0

# Example usage
start = (50, 50)
goal = (450, 450)

weight = 1  # distance weight
score_weight = 5

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create an empty list to store the paths
paths = []

number_of_paths = 8

for i in range(number_of_paths):
    direction = i * (360/number_of_paths)
    
    map_creation(image_source, threshold, direction)
    
    # Call path_plan_stack and store the result in the paths list
    image_path = 'split_image.png'
    score_map_path = 'trimmed_map.png'
    path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
    paths.append(path_result)

# Load the source image
source_image = Image.open(image_source)

# Plot all the paths in one plot
plt.figure()
plt.imshow(source_image, cmap='gray')
plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
plt.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')
for i, path in enumerate(paths):
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, label=f'Wind Heading {(i)*(360/number_of_paths)}')

plt.legend()
plt.title(f'A* Pathfinding with Score Map (All Directions)')
plt.show()
