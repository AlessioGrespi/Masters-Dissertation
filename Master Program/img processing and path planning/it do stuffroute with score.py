import numpy as np
import heapq
import matplotlib.pyplot as plt
from PIL import Image

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def astar(grid, score_map, start, goal, weight=1):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {point: float('inf') for point in np.ndindex(rows, cols)}
    g_score[start] = 0
    
    f_score = {point: float('inf') for point in np.ndindex(rows, cols)}
    f_score[start] = weight * euclidean_distance(start, goal)
    
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
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 1:
                tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    score_weight = 0  # Adjust this value as needed
                    f_score[neighbor] = g_score[neighbor] + weight * euclidean_distance(neighbor, goal) + score_weight * score_map[neighbor][0]  # Change score_map[neighbor] to score_map[neighbor][0]
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

# Example usage
image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'
start = (500, 500)
goal = (1900, 200)

weight = 2.0  # Adjust the weight factor here

image = load_image(image_path)
score_map = load_score_map(score_map_path)
path = astar(image, score_map, start, goal, weight)

if path:
    print("Path found:", path)
else:
    print("No path found.")




    

# Visualize the path on a plot
plt.imshow(image, cmap='gray')
plt.imshow(score_map, alpha=1, cmap='gist_gray')  # Ensure 'cmap' is set to 'hot'




plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
plt.scatter(goal[1], goal[0], color='blue', marker='x', label='Goal')
if path:
    path_y, path_x = zip(*path)
    plt.plot(path_x, path_y, color='red', label='Path')
plt.legend()
plt.title('A* Pathfinding')
plt.show()
