import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan
import img_processing_and_path_planning.e_kernels as k
import matplotlib.pyplot as plt  # Importing the correct module for plotting
from PIL import Image
import numpy as np
import csv

image_source = "render-7.png"
threshold = 256
map_translation = 0

# Example usage
start = (25, 25)
goal = (450,450)


def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

# Create an empty list to store the paths
paths = []

number_of_paths_distance = 8

weight = 1  # distance weight
score_weight = 1

image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'

direction = 0

path_costs = []
distance_costs = []
savings = []

# Define the CSV file path
csv_file_path = 'path_planning_results.csv'

# Open the CSV file in write mode
with open(csv_file_path, 'w', newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)

    # Write the header row
    csv_writer.writerow(['Distance', 'Score', 'Heading', 'Savings'])

    for i in range(7):
        score_weight = i + 2

        for j in range(8):
            weight = (j * 2) + 2

            for k in range(number_of_paths_distance):
                direction = k * (360/number_of_paths_distance) 

                map_creation(image_source, threshold, direction)

                # Call path_plan_stack and store the result in the paths list
                path_result, cost_result, distance_cost, saving = pathplan.path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path)
                paths.append(path_result)

                # Store the cost of the path
                path_costs.append(cost_result)
                distance_costs.append(distance_cost)
                savings.append(saving)
                print(f"distance: {weight}, score: {score_weight}, heading: {direction}, map: {image_source}, savings: {savings}")
                # Write the results to the CSV file
                csv_writer.writerow([weight, score_weight, direction, saving])


# Load the source image
source_image = Image.open("split_image_inverse.png")

# Load the score map image using PIL
score_map_image = Image.open(score_map_path)

# Convert the score map image to a NumPy array
score_map_data = np.array(score_map_image)











# Plot all the paths in one plot
plt.figure()
plt.imshow(source_image, cmap='gray')
plt.imshow(score_map_data, alpha=1, cmap='gist_gray')  # Ensure 'cmap' is set to 'hot'
plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
plt.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')

for i, path in enumerate(paths):
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, label=f'Score Weight {((i))}')

plt.legend(loc='upper right')
# plt.title(f'Score Weight: {score_weight}, Heading: {direction}')
plt.show()

print(f"distance: {weight}, score: {score_weight}, heading: {direction}, map: {image_source}, savings: {savings}")











""" # Plot cost versus weight
weights = range(4, number_of_paths_distance * 4, 1)
#plt.plot(weights, path_costs, marker='o', label='Path Costs')
#plt.plot(weights, distance_costs, marker='o', label='Distance Costs')  # Add this line
plt.plot(weights, savings, marker='o', label='Distance Costs')  # Add this line
plt.title(f'Cost Saving vs Distance Weight, Score Weight: {score_weight}')
plt.xlabel('Distance Weight')
plt.ylabel('Cost')
plt.legend()  # Add legend to differentiate between 'Path Costs' and 'Distance Costs'
plt.show() """