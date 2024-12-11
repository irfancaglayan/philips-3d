import cv2

# Open the image using OpenCV
img = cv2.imread('depth_anything_v2/bubble.jpg')

# Desired final dimensions
target_width, target_height = 960, 540

# Get the dimensions of the original image
original_height, original_width = img.shape[:2]

# Calculate the aspect ratio of the original and target
aspect_ratio = original_width / original_height
target_aspect_ratio = target_width / target_height

# Resize the image while maintaining the aspect ratio
if aspect_ratio > target_aspect_ratio:
    # Image is wider, so height is the limiting factor
    new_height = target_height
    new_width = int(target_height * aspect_ratio)
else:
    # Image is taller or equal, so width is the limiting factor
    new_width = target_width
    new_height = int(target_width / aspect_ratio)

# Resize the image
img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

# Calculate coordinates for cropping (center crop)
x_start = (new_width - target_width) // 2
y_start = (new_height - target_height) // 2
x_end = x_start + target_width
y_end = y_start + target_height

# Crop the image to the target size (960x540)
img_cropped = img_resized[y_start:y_end, x_start:x_end]

# Save the final image
cv2.imwrite('depth_anything_v2/bubble_resized.png', img_cropped)