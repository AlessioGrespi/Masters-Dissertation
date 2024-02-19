import img_processing_and_path_planning.a_img_setup as setup
import img_processing_and_path_planning.b_filtering as filtering
import img_processing_and_path_planning.c_lift_map_trimmer as lift_trimmer
import img_processing_and_path_planning.d_pathplanning as pathplan

image_source = "render-7.png"
threshold = 70
direction = 0
map_translation = 20

def map_creation(image_source, threshold, direction, map_translation):
    print(image_source)
    setup.setup_image(image_source, threshold, direction)
    setup.invert_image("grayscale_map.png", "grayscale_map.png") #for real world height map enable
    filtering.apply_ridge_filters("grayscale_map.png", direction, "ridge_map.png", map_translation)
    lift_trimmer.trim_reward_map("ridge_map.png", "split_image_inverse.png", "trimmed_map.png")
    setup.invert_image("ridge_map.png",f"render-7_{direction}_ridge_map.png")




for angle in range(24):
    direction = angle*15
    map_creation(image_source, threshold, direction, map_translation)
