import cv2
import numpy as np

def convert_image_to_grayscale_and_normalize(image_path, output_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if img is None:
        print("Error loading image")
        return
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Normalize the grayscale values to a specific range (contrast stretching)
    # For example, normalize between 50 and 200 to avoid pure black and pure white
    # normalized_gray = cv2.normalize(gray, None, 50, 200, cv2.NORM_MINMAX)
    
    # Convert the normalized grayscale image back to 3-channel (optional, if needed)
    normalized_gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    # Save the normalized grayscale image
    cv2.imwrite(output_path, normalized_gray_bgr)
    print(f"Image saved to {output_path}")

# Example usage
convert_image_to_grayscale_and_normalize('depth_pro/data/mountain.png', 'depth_pro/data/mountain_depth.png')