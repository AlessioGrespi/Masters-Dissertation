import cv2
import numpy as np
import random
import heapq

class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_obstacle = False
        self.children = []
        self.parent = None

    def distance_to(self, other):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def cost_to(self, other):
        return 1 + self.distance_to(other)

    def total_cost(self, start, end):
        return self.cost_to(start) + self.distance_to(end)


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
                process_quadtree(image, child, threshold)


def find_route(start, end):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (0, start))

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node == end:
            return construct_path(current_node)

        closed_set.add(current_node)

        for child in current_node.children:
            if child.is_obstacle or child in closed_set:
                continue

            new_cost = current_node.cost_to(child)
            if child not in open_list:
                heapq.heappush(open_list, (new_cost + child.distance_to(end), child))
            elif new_cost < current_node.cost_to(child):
                open_list.remove((current_node.cost_to(child) + child.distance_to(end), child))
                heapq.heappush(open_list, (new_cost + child.distance_to(end), child))
            child.parent = current_node

    return None


def construct_path(node):
    path = []
    while node:
        path.append((node.x + node.width // 2, node.y + node.height // 2))
        node = node.parent
    return path[::-1]


# Load the grayscale image
image = cv2.imread('output_image.png', cv2.IMREAD_GRAYSCALE)

# Define the threshold value
threshold = 70

# Perform quadtree process
quadtree = quadtree_process(image, threshold)

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

# Randomly pick a starting and ending point within the quadtree area
start_x = random.randint(0, image.shape[1])
start_y = random.randint(0, image.shape[0])
start_node = quadtree
while start_node.children:
    for child in start_node.children:
        if child.x <= start_x < child.x + child.width and child.y <= start_y < child.y + child.height:
            start_node = child
            break
end_x = random.randint(0, image.shape[1])
end_y = random.randint(0, image.shape[0])
end_node = quadtree
while end_node.children:
    for child in end_node.children:
        if child.x <= end_x < child.x + child.width and child.y <= end_y < child.y + child.height:
            end_node = child
            break

# Run A* algorithm to find the route
route = find_route(start_node, end_node)

# Overlay the route on top of the image and generated grid
if route:
    for i in range(len(route) - 1):
        cv2.line(image_colored, route[i], route[i + 1], (0, 255, 0), 2)

# Display the image with the quadtree overlay and route
cv2.imshow('Image with Quadtree Overlay and Route', image_colored)
cv2.waitKey(0)
cv2.destroyAllWindows()
