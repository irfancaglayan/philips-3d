import cv2
import numpy as np
import os

# RGB and depth image paths
rgb_image_path = ('depth_anything_v2/bubble_resized.png')
depth_image_path = ('depth_anything_v2/bubble_depth_normalized.png')

rgb_image = cv2.imread(rgb_image_path)
depth_image = cv2.imread(depth_image_path)

if rgb_image is None:
    raise FileNotFoundError(f"Error: Normal image is not found at {rgb_image_path}")
if depth_image is None:
    raise FileNotFoundError(f"Error: Depth image is not found at {depth_image_path}")

combined_image = np.hstack((rgb_image, depth_image))

# combined image path
combined_image_path = ("depth_anything_v2/bubble_combined.png")

cv2.imwrite(combined_image_path, combined_image)
print(f"Combined image saved at {combined_image_path}")
