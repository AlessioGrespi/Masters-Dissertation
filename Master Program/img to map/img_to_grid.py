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

def quadtree_process(image):
    height, width = image.shape[:2]
    quadtree = QuadTreeNode(0, 0, width, height)
    process_quadtree(image, quadtree)
    return quadtree

def process_quadtree(image, quadtree):
    x, y, w, h = quadtree.x, quadtree.y, quadtree.width, quadtree.height
    region = image[y:y+h, x:x+w]
    min_value = np.min(region)

    if min_value != 0:
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
                process_quadtree(image, child)

# Draw quadtree overlay on the new image
def draw_quadtree(node, image):
    if node.is_obstacle:
        cv2.rectangle(image, (node.x, node.y), (node.x + node.width, node.y + node.height), (0, 0, 255, 255), 2)
    else:
        for child in node.children:
            draw_quadtree(child, image)

def img_to_quadtree(image_path, background_path, output_path_overlay, output_path_merged):
    # Load the grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Perform quadtree process
    quadtree = quadtree_process(image)

    # Create a colored version of the image
    image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Create a new image with transparent background for the quadtree overlay
    image_with_overlay = np.zeros((image_colored.shape[0], image_colored.shape[1], 4), dtype=np.uint8)
    image_with_overlay[:, :, 3] = 0

    # Draw the quadtree on the transparent background image
    draw_quadtree(quadtree, image_with_overlay)

    # Save the image with quadtree overlay and transparent background to a PNG file
    cv2.imwrite(output_path_overlay, image_with_overlay)

    # Load the background image
    background = cv2.imread(background_path)

    # Resize the background image to match the grayscale image dimensions
    background = cv2.resize(background, (image.shape[1], image.shape[0]))

    # Merge the colored image and the background image
    image_merged = cv2.addWeighted(image_colored, 0.5, background, 0.5, 0)

    # Draw the quadtree on the merged image
    draw_quadtree(quadtree, image_merged)

    # Save the image with quadtree overlay on the background to a PNG file
    cv2.imwrite(output_path_merged, image_merged)

# Specify the paths for input image, background image, and output files
image_path = "Map+Ridge.png"
background_path = "Map+Ridge.png"
output_path_overlay = "output_overlay.png"
output_path_merged = "output_merged.png"

# Call the function to generate the two output images
img_to_quadtree(image_path, background_path, output_path_overlay, output_path_merged)
