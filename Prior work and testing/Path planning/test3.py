import cv2
import numpy as np
import matplotlib.pyplot as plt

def quadtree_process(image, threshold):
    height, width = image.shape[:2]
    quadtree = QuadTreeNode(0, 0, width, height)
    process_quadtree(image, quadtree, threshold)
    return quadtree

def process_quadtree(image, quadtree, threshold):
    x, y, w, h = quadtree.x, quadtree.y, quadtree.width, quadtree.height
    region = image[y:y+h, x:x+w]
    max_value = np.max(region)

    if max_value < threshold:
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


class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_obstacle = False
        self.children = []

def quadtree_to_map(quadtree):
    map = np.zeros((quadtree.height, quadtree.width), dtype=np.uint8)
    populate_map(quadtree, map)
    return map

def populate_map(node, map):
    if node.is_obstacle:
        map[node.y:node.y + node.height, node.x:node.x + node.width] = 255
    else:
        for child in node.children:
            populate_map(child, map)

# Load the grayscale image
image = cv2.imread('output_image.png', cv2.IMREAD_GRAYSCALE)

# Define the threshold value
threshold = 70

# Perform quadtree process
quadtree = quadtree_process(image, threshold)

# Convert quadtree to map
map = quadtree_to_map(quadtree)

# Plot the map
plt.imshow(map, cmap='gray')
plt.title('Map')
plt.show()
