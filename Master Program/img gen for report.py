import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan

image_source = "render-5.png"
threshold = 255
direction = 180
map_translation = 20

def map_creation(image_source, threshold, direction, map_translation):
    setup.setup_image(image_source, threshold, direction)
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map_{}.png".format(direction), map_translation)
    setup.invert_image("ridge_map_{}.png".format(direction),"ridge_map_{}.png".format(direction))
    #lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")

map_creation(image_source, threshold, direction, map_translation)

""" for angle in range(24):
    direction = angle*15
    map_creation(image_source, threshold, direction, map_translation)
 """
""" 
# Example usage
image_path = 'split_image.png'
score_map_path = 'trimmed_map.png'
start = (250, 250)
goal = (1900, 200)

weight = 5  # distance weight
score_weight = 10

pathplan.path_plan(start, goal, weight, score_weight, image_path, score_map_path) """