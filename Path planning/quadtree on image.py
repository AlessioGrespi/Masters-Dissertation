import cv2
import numpy as np
import pickle

def dump_quadtree_to_file(quadtree, filename):
    with open(filename, 'wb') as file:
        pickle.dump(quadtree, file)

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

# Load the grayscale image
image = cv2.imread('output_image.png', cv2.IMREAD_GRAYSCALE)

# Define the threshold value
threshold = 70

# Perform quadtree process
quadtree = quadtree_process(image, threshold)

dump_quadtree_to_file(quadtree, 'quadtree.pkl')

# Create a colored version of the image
image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Draw quadtree overlay on the colored image
def draw_quadtree(node, image):
    if node.is_obstacle:
        cv2.rectangle(image, (node.x, node.y), (node.x + node.width, node.y + node.height), (0, 0, 255), 2)
    else:
        for child in node.children:
            draw_quadtree(child, image)

draw_quadtree(quadtree, image_colored)

# Display the image with the quadtree overlay
cv2.imshow('Image with Quadtree Overlay', image_colored)
cv2.waitKey(0)
cv2.destroyAllWindows()
