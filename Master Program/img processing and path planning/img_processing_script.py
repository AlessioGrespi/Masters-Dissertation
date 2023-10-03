import a_img_setup as setup
import b_filtering as filtering
import c_lift_map_trimmer as lift_trimmer
import d_pathplanning as pathplan

image_source = "render-5.png"
threshold = 70
direction = 0

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png")
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

map_creation(image_source, threshold, direction)
""" 
# Example usage
image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'
start = (250, 250)
goal = (1900, 200)

weight = 5  # distance weight
score_weight = 10

pathplan.path_plan(start, goal, weight, score_weight, image_path, score_map_path) """