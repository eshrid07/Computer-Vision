import cv2
import numpy as np
import json

# Default Values
image_height = 480
image_width = 640
ground_distance = 2000
output_path = "depth_image.png"

def main():
    objects_data = None
    try:
        with open('/home/shri/development/Computer-Vision/tools/Synthetic_Depth_Image/box_dimensions.json', 'r') as file:
            objects_data = json.load(file)
    except:
        print("Issue with the box_dimensions.json file")

    depth_image = np.zeros((image_height, image_width), dtype=np.uint16)
    depth_image[0:image_height, 0:image_width] = float(ground_distance)
    for i in objects_data.keys():
        if "box" in i:
            # Read the Values
            x1, y1 = objects_data[i]["x1"], objects_data[i]["y1"]
            x2, y2= objects_data[i]["x2"], objects_data[i]["y2"]
            depth = objects_data[i]["depth"]
            if x2 < x1 or y2 < y1 or depth < 100:
                print("Skipping {i} because either start and end points are not correct or depth < 100")
                continue
            
            # Limit the points within the image
            x1 = 0 if x1 < 0 else image_width-1 if x1 >= image_width else x1
            x2 = 0 if x2 < 0 else image_width-1 if x2 >= image_width else x2
            y1 = 0 if y1 < 0 else image_height-1 if y1 >= image_height else y1
            y2 = 0 if y2 < 0 else image_height-1 if y2 >= image_height else y2

            # Check for Overlap
            region = depth_image[y1:y2, x1:x2]
            if np.all(region == ground_distance):
                depth_image[y1:y2, x1:x2] = float(depth)
            else:
                print("skipping the box because of overlap")
        else:
            print("some other object")
    cv2.imwrite(output_path, depth_image)
        
if __name__ == "__main__":
    main()