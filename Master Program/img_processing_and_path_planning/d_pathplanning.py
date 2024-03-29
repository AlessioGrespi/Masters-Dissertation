"""
A* path planning with a score map from the thermals. 

FILE IS COMPLETE AS OF 25/8/23 DO NOT MODIFY FURTHER
"""

import numpy as np
import heapq
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import CubicSpline

""" 
def path_plan(start, goal, weight, score_weight, image_path, score_map_path, direction):
    def euclidean_distance(p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def astar(grid, score_map, start, goal, weight, score_weight,):
        rows, cols = grid.shape
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {point: float('inf') for point in np.ndindex(rows, cols)}
        g_score[start] = 0
        
        f_score = {point: float('inf') for point in np.ndindex(rows, cols)}
        f_score[start] = weight * manhattan_distance(start, goal)
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 1:
                    tentative_g_score = g_score[current] + manhattan_distance(current, neighbor)  # Use euclidean_distance
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + weight * manhattan_distance(neighbor, goal) + score_weight * score_map[neighbor][0]  # Change score_map[neighbor] to score_map[neighbor][0]
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # No path found


    def load_image(image_path):
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
        img_array = np.array(img)
        binary_image = (img_array > 128).astype(int)  # Convert to binary image
        return binary_image

    def load_score_map(score_map_path):
        score_map_img = Image.open(score_map_path)
        score_map_array = np.array(score_map_img)
        return score_map_array

    def smooth_path_with_spline(path):
        # Extract x and y coordinates from the path
        x, y = zip(*path)
        
        # Create a cubic spline for the path
        t = range(len(path))
        cs_x = CubicSpline(t, x)
        cs_y = CubicSpline(t, y)
        
        # Interpolate points along the spline
        num_points = 100  # Adjust as needed
        t_new = np.linspace(0, len(path) - 1, num_points)
        smoothed_path = [(cs_x(t), cs_y(t)) for t in t_new]
        
        return smoothed_path



    image = load_image(image_path)
    score_map = load_score_map(score_map_path)
    path = astar(image, score_map, start, goal, weight, score_weight)

    if path:
        print("Path found:", path)
        smoothed_path = smooth_path_with_spline(path)
        print("Smoothed Path:", smoothed_path)
    else:
        print("No path found.")

     # Visualize the path on a plot
    plt.imshow(image, cmap='gray')
    plt.imshow(score_map, alpha=0.5, cmap='hot')  # Ensure 'cmap' is set to 'hot'
     
    

    # Ensure 'cmap' is set to 'hot' for the score_map
    cmap = 'winter'

    # Define a threshold for the image to determine what is considered black
    black_threshold = 256  # You can adjust this threshold as needed

    # Create a mask for fully opaque regions in the image
    mask = np.where(image <= black_threshold, 1, 0)

    # Calculate the modified alpha parameter
    alpha = 0.5  # Default alpha for other regions
    alpha = alpha * (1 - mask) + 1 * mask  # Use alpha=1 for black regions

    # Visualize the path on a plot
    plt.imshow(image, cmap='gray')
    plt.imshow(score_map, alpha=alpha, cmap=cmap)  # Use the modified alpha parameter
    #
    
    
    
    plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
    plt.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, color='blue', label='Path')
        smoothed_path_y, smoothed_path_x = zip(*smoothed_path)
        #plt.plot(smoothed_path_x, smoothed_path_y, color='green', label='Smoothed Path')
    plt.legend()
    plt.title(f'A* Pathfinding with Score Map and Wind Heading {(direction)}')
    plt.show()

 """


def path_plan_stack(start, goal, weight, score_weight, image_path, score_map_path):
    def euclidean_distance(p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def astar(grid, score_map, start, goal, weight, score_weight):

        current_cost = 0
        distance_cost = 0
        savings = 0
        rows, cols = grid.shape
        open_set = []
        heapq.heappush(open_set, (0, start, 0, 0, 0))  # Add a third element for the cost

        came_from = {}
        g_score = {point: float('inf') for point in np.ndindex(rows, cols)}
        g_score[start] = 0

        f_score = {point: float('inf') for point in np.ndindex(rows, cols)}
        f_score[start] = weight * euclidean_distance(start, goal)

        while open_set:
            _, current, current_cost, distance_cost, savings = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                print(f"Path found with cost {current_cost}")
                return path, current_cost, distance_cost, savings

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 1:
                    tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)


                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + weight * euclidean_distance(neighbor, goal) + score_weight * score_map[neighbor][0]
                        
                        #corrected_cost = current_cost + (1 * (score_map[neighbor][0] / 255))

                        heapq.heappush(open_set, (f_score[neighbor], neighbor, current_cost + ((1*(score_map[neighbor][0] / 255))), distance_cost + 1, savings + (1-(score_map[neighbor][0] / 255))))  # Update cost

                    #print(f"Current Cost: {current_cost} | Distance Score: {weight * euclidean_distance(neighbor, goal)} | Score score: {score_map[neighbor][0]}")
                        

        print("No path found.")
        return None  # No path found

    def load_image(image_path):
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
        img_array = np.array(img)
        binary_image = (img_array > 128).astype(int)  # Convert to binary image
        return binary_image

    def load_score_map(score_map_path):
        score_map_img = Image.open(score_map_path)
        score_map_array = np.array(score_map_img)
        return score_map_array

    image = load_image(image_path)
    score_map = load_score_map(score_map_path)
    path = astar(image, score_map, start, goal, weight, score_weight)

    if path:
        return path
    else:
        return None  # No path found


