import cv2
import numpy as np

def convert_video_to_grayscale_and_normalize(video_path):
    # Open the video capture
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create a video writer to save the normalized grayscale video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' instead of 'XVID'
    out = cv2.VideoWriter('ski_depth_normalized.mp4', fourcc, fps, (width, height))
    
    # Read and convert each frame to grayscale and normalize
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Normalize the grayscale values to a specific range (contrast stretching)
        # For example, normalize between 50 and 200 to avoid pure black and pure white
        normalized_gray = cv2.normalize(gray, None, 50, 200, cv2.NORM_MINMAX)
        
        # Convert the grayscale frame back to 3-channel (required for video writer)
        normalized_gray_bgr = cv2.cvtColor(normalized_gray, cv2.COLOR_GRAY2BGR)
        
        # Write the normalized grayscale frame to the output video
        out.write(normalized_gray_bgr)
    
    # Release the video capture and writer
    cap.release()
    out.release()

# Example usage
convert_video_to_grayscale_and_normalize('depth_crafter/ski_depth_final.mp4')
