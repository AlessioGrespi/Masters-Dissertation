import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan
import matplotlib.pyplot as plt  # Importing the correct module for plotting
from PIL import Image

image_source = "render-5.png"
threshold = 70
map_translation = 20

# Example usage
start = (250, 200)
goal = (1500, 1600)

weight = 9  # distance weight
score_weight = 6



def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create an empty list to store the paths
paths = []

number_of_paths = 1

for i in range(number_of_paths):
    #direction = i * (360/number_of_paths)
    direction = 270 
    map_creation(image_source, threshold, direction)
    
    # Call path_plan_stack and store the result in the paths list
    image_path = 'split_image.png'
    score_map_path = 'trimmed_map.png'
    path_result = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
    paths.append(path_result)

    # New goal coordinates
    new_goal = (1900, 200)

    # Add a new path planning step from (1500, 1600) to (200, 1900)
    path_result2 = pathplan.path_plan_stack(goal, new_goal, weight, score_weight, image_path, score_map_path)
    paths.append(path_result2)

        # Add a new path planning step from (1500, 1600) to (200, 1900)
    path_result3 = pathplan.path_plan_stack(new_goal, start, weight, score_weight, image_path, score_map_path)
    paths.append(path_result3)

# Load the source image
source_image = Image.open("ridge_map.png")

# Plot all the paths in one plot
plt.figure()
plt.imshow(source_image, cmap='gray')
plt.scatter(start[1], start[0], color='green', marker='x', label='A')
plt.scatter(goal[1], goal[0], color='blue', marker='x', label='B')
plt.scatter(new_goal[1], new_goal[0], color='red', marker='x', label='C')
for i, path in enumerate(paths):
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, label=f'Part {i+1}')

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title(f'Pathfinding between points, Wind direction: {direction}')
plt.show()
