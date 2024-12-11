import cv2
import numpy as np

image = cv2.imread('depth_anything_v2/bubble_combined.png')

hex_header = 'f10140800000c42dd3aff2140000000000000000000000000000000036958221'
# .s3d file format headers:
# 2D-plus-Depth: f10140800000c42dd3aff2140000000000000000000000000000000036958221
# Declipse - no redundant data: f10140800000c42dd3aff2149a0000000000000000000000000000006bf6c689
# Declipse - full bg data: f10140800000c42dd3aff214ef0000000000000000000000000000002ff0c45f

# Header control
if len(hex_header) != 64:
    raise ValueError("Header must be exactly 64 hexadecimal characters (32 bytes)")

# Convert the hexadecimal header to bytes
header_bytes = bytes.fromhex(hex_header)

# Convert the header bytes to a list of bits
header_bits = []
for byte in header_bytes:
    for i in range(8):
        header_bits.append((byte >> (7 - i)) & 1)

height, width, _ = image.shape
bit_idx = 0

# Loop through the even blue sub-pixels
for y in range(height):
    for x in range(0, width, 2):  # Step by 2 to get even pixels
        if bit_idx < len(header_bits):
            b = image[y, x, 0]  # OpenCV uses BGR order
            msb = header_bits[bit_idx]  # Get the bit to embed
            # Modify the MSB of the blue value
            b = (b & 0x7F) | (msb << 7)
            image[y, x, 0] = b  # Update the blue channel
            bit_idx += 1
        else:
            break
    if bit_idx >= len(header_bits):
        break

# Save the modified image
output_path = 'depth_anything_v2/bubble_header.png'
cv2.imwrite(output_path, image)

print(f"Header embedded and image saved to {output_path}")