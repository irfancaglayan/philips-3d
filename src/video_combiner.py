import cv2

def combine_videos_horizontally(video_path1, video_path2):
    # Open the video captures
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    # Check if the video files were opened successfully
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error opening video files")
        return
    
    # Get the video properties for both videos
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Find out which video has the lower resolution
    if (width1 * height1) <= (width2 * height2):
        target_width, target_height = width1, height1
        resize_needed = 2  # Resize second video to match first
    else:
        target_width, target_height = width2, height2
        resize_needed = 1  # Resize first video to match second
    
    print(f"Resizing video {resize_needed} to match the lower resolution video with dimensions: {target_width}x{target_height}")
    
    # Create a video writer to save the combined video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = min(fps1, fps2)  # Use the lower FPS for the combined video
    out = cv2.VideoWriter('depth_flow/cats_combined.mp4', fourcc, fps, (target_width * 2, target_height))
    
    # Read and combine each frame
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            break
        
        # Resize the higher resolution video frame to match the lower resolution one
        if resize_needed == 1:
            frame1 = cv2.resize(frame1, (target_width, target_height))
        elif resize_needed == 2:
            frame2 = cv2.resize(frame2, (target_width, target_height))
        
        # Combine the frames horizontally
        combined_frame = cv2.hconcat([frame1, frame2])
        
        # Write the combined frame to the output video
        out.write(combined_frame)
    
    # Release the video captures and writer
    cap1.release()
    cap2.release()
    out.release()

# Example usage
combine_videos_horizontally('depth_flow/cats_vid_depth_pro.mp4', 'depth_flow/cats_depth_depth_pro.mp4')