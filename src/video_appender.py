import cv2

def append_videos(video_path1, video_path2, output_path):
    # Open the video captures
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    # Check if the video files were opened successfully
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error opening video files")
        return
    
    # Get the properties of the first video
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Get the properties of the second video
    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Adjust resolution to the lower one
    if (width1 * height1) < (width2 * height2):
        target_width, target_height = width1, height1
        resize_needed = 2  # Resize second video to match the first
    else:
        target_width, target_height = width2, height2
        resize_needed = 1  # Resize first video to match the second

    print(f"Resizing video {resize_needed} to match the lower resolution video with dimensions: {target_width}x{target_height}")
    
    # Create a video writer to save the appended video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps1, (target_width, target_height))
    
    # Write frames from the first video
    while True:
        ret1, frame1 = cap1.read()
        if not ret1:
            break
        
        # Resize frame1 if necessary
        if resize_needed == 1:
            frame1 = cv2.resize(frame1, (target_width, target_height))
        
        # Write the frame
        out.write(frame1)
    
    # Write frames from the second video
    while True:
        ret2, frame2 = cap2.read()
        if not ret2:
            break
        
        # Resize frame2 if necessary
        if resize_needed == 2:
            frame2 = cv2.resize(frame2, (target_width, target_height))
        
        # Write the frame
        out.write(frame2)
    
    # Release the video captures and writer
    cap1.release()
    cap2.release()
    out.release()
    print(f"Videos appended and saved to {output_path}")

# Example usage
append_videos('depth_flow/cats_combined.mp4', 'depth_flow/mountains_combined.mp4', 'depth_flow/appended.mp4')
