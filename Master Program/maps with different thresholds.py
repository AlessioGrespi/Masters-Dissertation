import img_processing_and_path_planning.a_img_setup as img_setup

image_source = "render-7.png"

img_setup.convert_to_grayscale(image_source, "grayscale_map.png")

threshold_step = 16
thresholds = 256 / threshold_step
thresholds = 17

for i in range(thresholds):
    threshold = i * threshold_step
    img_setup.img_split(image_source, threshold, f"render-7_img_map_{threshold}.png")
    #img_setup.invert_image(f"render-7_img_map_{threshold}.png",f"render-7_img_map_{threshold}.png")
