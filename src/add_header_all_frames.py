import cv2
import numpy as np

# Input and output video paths
input_video_path = 'depth_crafter/combined_ski.mp4'
output_video_path = 'depth_crafter/combined_ski_header.mp4'

# Predefined header
#s3d
hex_header = 'f10140800000c42dd3aff2140000000000000000000000000000000036958221'
#v3d
#hex_header = "f102408000001f3a7b38f2140000000000000000000000000000000036958221"

# Header control
if len(hex_header) != 64:
    raise ValueError("Header must be exactly 64 hexadecimal characters (32 bytes)")

# Convert the hexadecimal header to bytes and bits
header_bytes = bytes.fromhex(hex_header)
header_bits = []
for byte in header_bytes:
    for i in range(8):
        header_bits.append((byte >> (7 - i)) & 1)

# Open the video capture and read the video
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Function to embed header into a frame
def embed_header_to_frame(frame, header_bits):
    bit_idx = 0
    for y in range(frame.shape[0]):
        for x in range(0, frame.shape[1], 2):  # Step by 2 for even pixels
            if bit_idx < len(header_bits):
                b = frame[y, x, 0]  # OpenCV uses BGR order
                msb = header_bits[bit_idx]  # Get the bit to embed
                # Modify the MSB of the blue value
                b = (b & 0x7F) | (msb << 7)
                frame[y, x, 0] = b  # Update the blue channel
                bit_idx += 1
            else:
                return frame
    return frame

# Process the video
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Embed header in every frame
    frame = embed_header_to_frame(frame, header_bits)
    
    out.write(frame)
    frame_count += 1

# Release everything
cap.release()
out.release()

print(f"Header embedded into all frames and saved to {output_video_path}")