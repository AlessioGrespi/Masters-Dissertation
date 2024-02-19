import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan
import matplotlib.pyplot as plt
import numpy as np
import csv
from PIL import Image

image_source = "render-5.png"
threshold = 70
map_translation = 20

# Example usage
start = (250, 200)
goal = (1500, 100)

weight = 9  # distance weight
score_weight = 6

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create lists to store the paths and costs
paths = []
current_costs = []
distance_costs = []
savings_list = []

number_of_paths = 8

for i in range(number_of_paths):
    direction = i * (360 / number_of_paths)
    map_creation(image_source, threshold, direction)
    
    # Call path_plan_stack and store the result in the paths list
    image_path = 'split_image.png'
    score_map_path = 'trimmed_map.png'
    path, current_cost, distance_cost, savings = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
    
    # Append results to the lists
    paths.append(path)
    current_costs.append(current_cost)
    distance_costs.append(distance_cost)
    savings_list.append(savings)

# Load the source image
source_image = Image.open("split_image.png")

# Plot all the paths in one plot
plt.figure()
plt.imshow(source_image, cmap='gray')
plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
plt.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')

for i, path in enumerate(paths):
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, label=f'Wind Heading {(i)*(360/number_of_paths)}')

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title(f'Pathfinding (all wind directions)')
plt.show()

# Scatter plot for costs
plt.figure()
wind_headings = np.arange(0, 360, 360 / number_of_paths)
plt.scatter(wind_headings, current_costs, label='Current Cost')
plt.scatter(wind_headings, distance_costs, label='Distance Cost')
plt.scatter(wind_headings, savings_list, label='Savings')
plt.xlabel('Wind Heading (degrees)')
plt.ylabel('Cost')
plt.legend()
plt.title('Costs vs Wind Heading')
plt.show()

# Write data to CSV
csv_data = list(zip(wind_headings, current_costs, distance_costs, savings_list))
csv_file_path = 'cost_data.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Wind Heading', 'Current Cost', 'Distance Cost', 'Savings'])
    csv_writer.writerows(csv_data)

print(f'Data written to {csv_file_path}')
