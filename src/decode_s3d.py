import cv2
import numpy as np

image = cv2.imread('0001.png')

height, width, _ = image.shape

header_bits = []

for y in range(height):
    for x in range(0, width, 2):  # even pixels
        b = image[y, x, 0]
        msb = (b & 0x80) >> 7  # extract the most significant bit (MSB)
        header_bits.append(msb)  # append the MSB

        if len(header_bits) == 32 * 8:
            break
    if len(header_bits) == 32 * 8:
        break

# Convert the list of bits to bytes
header_bytes = bytearray()
for i in range(0, len(header_bits), 8):
    byte = 0
    for bit in header_bits[i:i+8]:
        byte = (byte << 1) | bit
    header_bytes.append(byte)

# Print the header in hexadecimal
header_hex = ''.join(format(byte, '02x') for byte in header_bytes)
print("Header (in hexadecimal):", header_hex)
