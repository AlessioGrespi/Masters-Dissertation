import a_img_setup as setup
import b_filtering as filtering
import c_lift_map_trimmer as lift_trimmer
import d_pathplanning as pathplan

image_source = "render-7.png"
threshold = 256
direction = 90
map_translation = 0

def map_creation(image_source, threshold, direction):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

map_creation(image_source, threshold, direction)

# Example usage
image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'
start = (100, 100)
goal = (400, 400)

weight = 1  # distance weight
score_weight = 5

pathplan.path_plan(start, goal, weight, score_weight, image_path, score_map_path)    