import cv2
import numpy as np

class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_obstacle = False
        self.children = []
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


def quadtree_process(image, threshold):
    height, width = image.shape[:2]
    quadtree = QuadTreeNode(0, 0, width, height)
    process_quadtree(image, quadtree, threshold)
    return quadtree


def process_quadtree(image, quadtree, threshold):
    x, y, w, h = quadtree.x, quadtree.y, quadtree.width, quadtree.height
    region = image[y:y + h, x:x + w]
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
                child.set_parent(quadtree)
                process_quadtree(image, child, threshold)


def draw_quadtree(node, image):
    if node.is_obstacle:
        cv2.rectangle(image, (node.x, node.y), (node.x + node.width, node.y + node.height), (0, 0, 255), 2)
    else:
        for child in node.children:
            draw_quadtree(child, image)


def generate_path(start, end):
    path = []
    current_node = end

    while current_node is not None and current_node != start:
        if current_node.x is not None and current_node.y is not None and current_node.width is not None and current_node.height is not None:
            path.append((current_node.x + current_node.width // 2, current_node.y + current_node.height // 2))
        current_node = current_node.parent

    if start.x is not None and start.y is not None and start.width is not None and start.height is not None:
        path.append((start.x + start.width // 2, start.y + start.height // 2))
    path.reverse()
    return path


def overlay_path(image, path, start_point, end_point, quadtree):
    image_overlay = image.copy()
    x_offset, y_offset = quadtree.x, quadtree.y
    for point in path:
        adjusted_point = (point[0] + x_offset, point[1] + y_offset)
        cv2.circle(image_overlay, adjusted_point, 2, (0, 255, 0), -1)
    adjusted_start = (start_point[0] + x_offset, start_point[1] + y_offset)
    adjusted_end = (end_point[0] + x_offset, end_point[1] + y_offset)
    cv2.circle(image_overlay, adjusted_start, 3, (255, 0, 0), -1)
    cv2.circle(image_overlay, adjusted_end, 3, (0, 0, 255), -1)
    return image_overlay



# Load the grayscale image
image = cv2.imread('output_image.png', cv2.IMREAD_GRAYSCALE)

# Define the threshold value
threshold = 70

# Perform quadtree process
quadtree = quadtree_process(image, threshold)

# Create a colored version of the image
image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# Draw quadtree overlay on the colored image
draw_quadtree(quadtree, image_colored)

# Randomly generate start and end points
start_node = quadtree.children[np.random.randint(0, len(quadtree.children))]
end_node = None

# Find a valid end node
while end_node is None or end_node.is_obstacle:
    end_node = quadtree.children[np.random.randint(0, len(quadtree.children))]

# Generate the path using A*
path = generate_path(start_node, end_node)

# Overlay the path on the image
image_with_path = overlay_path(image_colored, path, (start_node.x + start_node.width // 2, start_node.y + start_node.height // 2), (end_node.x + end_node.width // 2, end_node.y + end_node.height // 2), quadtree)


# Display the image with the path overlay
cv2.imshow('Image with Path Overlay', image_with_path)
cv2.waitKey(0)
cv2.destroyAllWindows()