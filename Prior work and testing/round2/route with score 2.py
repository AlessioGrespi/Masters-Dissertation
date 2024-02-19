import numpy as np
import heapq
import matplotlib.pyplot as plt
from PIL import Image

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class QuadtreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = [None, None, None, None]
        self.is_leaf = True

# Modify the construct_quadtree function
def construct_quadtree(grid, x, y, width, height, max_depth, threshold):
    node = QuadtreeNode(x, y, width, height)
    if max_depth <= 0 or np.sum(grid[y:y+height, x:x+width]) <= threshold:
        return node
    
    mid_x = x + width // 2
    mid_y = y + height // 2
    
    # Check if the entire quadrant is traversable
    quadrant_traversable = np.all(grid[y:mid_y, x:mid_x]) and \
                           np.all(grid[y:mid_y, mid_x:x+width]) and \
                           np.all(grid[mid_y:y+height, x:mid_x]) and \
                           np.all(grid[mid_y:y+height, mid_x:x+width])
    
    if not quadrant_traversable:
        return node
    
    node.children[0] = construct_quadtree(grid, x, y, width // 2, height // 2, max_depth - 1, threshold)
    node.children[1] = construct_quadtree(grid, mid_x, y, width // 2, height // 2, max_depth - 1, threshold)
    node.children[2] = construct_quadtree(grid, x, mid_y, width // 2, height // 2, max_depth - 1, threshold)
    node.children[3] = construct_quadtree(grid, mid_x, mid_y, width // 2, height // 2, max_depth - 1, threshold)
    
    node.is_leaf = False
    return node

def query_quadtree(node, x, y):
    if node.is_leaf:
        return node
    
    quadrant_index = 0
    if x >= node.x + node.width // 2:
        quadrant_index += 1
    if y >= node.y + node.height // 2:
        quadrant_index += 2
    
    return query_quadtree(node.children[quadrant_index], x, y)

def astar_with_quadtree(quadtree_root, grid, score_map, start, goal, weight=1):
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
        
        current_node = query_quadtree(quadtree_root, current[1], current[0])
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                neighbor_node = query_quadtree(quadtree_root, neighbor[1], neighbor[0])
                
                if current_node.is_leaf and neighbor_node.is_leaf:
                    if grid[neighbor] == 1:
                        tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)
                        if tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            score_weight = 10  # Adjust this value as needed
                            f_score[neighbor] = g_score[neighbor] + weight * euclidean_distance(neighbor, goal) + score_weight * score_map[neighbor]
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
start = (10, 10)
goal = (1900, 200)


weight = 2.0  # Adjust the weight factor here
max_depth = 4  # Adjust the maximum depth of the Quadtree
threshold = 5  # Adjust the threshold for Quadtree leaf nodes

image = load_image(image_path)
score_map = load_score_map(score_map_path)
quadtree_root = construct_quadtree(image, 0, 0, image.shape[1], image.shape[0], max_depth, threshold)
path = astar_with_quadtree(quadtree_root, image, score_map, start, goal, weight)

# Visualize the path on a plot
fig, ax = plt.subplots()
ax.imshow(image, cmap='gray')
ax.imshow(score_map, alpha=0.5, cmap='hot')
ax.scatter(start[1], start[0], color='green', marker='o', label='Start')
ax.scatter(goal[1], goal[0], color='red', marker='x', label='Goal')
if path:
    path_y, path_x = zip(*path)
    ax.plot(path_x, path_y, color='blue', label='Path')

# Function to recursively draw the Quadtree nodes
def draw_quadtree(node, ax):
    if node.is_leaf:
        rect = plt.Rectangle((node.x, node.y), node.width, node.height, fill=False, color='orange', linewidth=0.7)
        ax.add_patch(rect)
    else:
        for child in node.children:
            draw_quadtree(child, ax)

# Draw the Quadtree nodes on the plot
draw_quadtree(quadtree_root, ax)

ax.legend()
ax.set_title('A* Pathfinding with Quadtree and Score Map')
plt.show()