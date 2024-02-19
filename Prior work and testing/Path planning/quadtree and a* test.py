import cv2
import numpy as np
import pickle

class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_obstacle = False
        self.children = []

def quadtree_process(image, threshold):
    height, width = image.shape[:2]
    quadtree = QuadTreeNode(0, 0, width, height)
    process_quadtree(image, quadtree, threshold)
    return quadtree

def process_quadtree(image, quadtree, threshold):
    x, y, w, h = quadtree.x, quadtree.y, quadtree.width, quadtree.height
    region = image[y:y+h, x:x+w]
    min_value = np.min(region)

    if min_value > threshold:
        quadtree.is_obstacle = True
    else:
        if w > 1 and h > 1:
            quadtree.children = []
            half_w, half_h = w // 2, h // 2
            quadtree.children.append(QuadTreeNode(x, y, half_w, half_h))
            quadtree.children.append(QuadTreeNode(x + half_w, y, half_w, half_h))
            quadtree.children.append(QuadTreeNode(x, y + half_h, half_w, half_h))
            quadtree.children.append(QuadTreeNode(x + half_w, y + half_h, half_w, half_h))

            for child in quadtree.children:
                process_quadtree(image, child, threshold)


# Load the grayscale image
image = cv2.imread('split-image.png', cv2.IMREAD_GRAYSCALE)

# Define the threshold value
threshold = 70

# Perform quadtree process
quadtree = quadtree_process(image, threshold)

# Save the quadtree object to a file using pickle
with open('quadtree.pkl', 'wb') as file:
    pickle.dump(quadtree, file)

# Pathfinding using the quadtree
def find_path(start, goal, quadtree):
    if not quadtree.is_obstacle:
        if not quadtree.children:
            return [(quadtree.x + quadtree.width // 2, quadtree.y + quadtree.height // 2)]
        else:
            for child in quadtree.children:
                if is_point_inside(start, child) and is_point_inside(goal, child):
                    return find_path(start, goal, child)
    return []

def is_point_inside(point, quadtree):
    x, y = point
    return quadtree.x <= x < quadtree.x + quadtree.width and quadtree.y <= y < quadtree.y + quadtree.height

# Define start and goal points
start_point = (10, 10)
goal_point = (200, 200)

# Find path using the quadtree
path = find_path(start_point, goal_point, quadtree)

# Print the path
print("Path:")
for point in path:
    print(point)

# Display the quadtree overlay on the image
image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

def draw_quadtree(node, image):
    if node.is_obstacle:
        cv2.rectangle(image, (node.x, node.y), (node.x + node.width, node.y + node.height), (0, 0, 255), 2)
    else:
        for child in node.children:
            draw_quadtree(child, image)

draw_quadtree(quadtree, image_colored)

# Draw the path on the image
if path:
    for i in range(len(path) - 1):
        cv2.line(image_colored, path[i], path[i + 1], (0, 255, 0), 2)

# Display the image with the quadtree overlay and path
cv2.imshow('Image with Quadtree Overlay and Path', image_colored)
cv2.waitKey(0)
cv2.destroyAllWindows()
