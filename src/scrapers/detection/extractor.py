import json
import os

import cv2
import numpy as np
from PIL import Image

# Load the image from the file "frame.jpg"
image = Image.open("frame.jpg")

# Get the dimensions of the image
# width: The width of the image
# height: The height of the image
width, height = image.size
print("Dimensions de l'image:", width, "x", height)

# Initialize an empty dictionary to store the coordinates of the characters
characters = {}

# Define the coordinates of the characters
# The image is divided into 12 sections, each containing a character
# The coordinates of each character are calculated based on its position in the image
for i in range(0, 12):
    if i > 5:
        offset = 787
        current = i - 6
    else:
        offset = 0
        current = i
    y1 = 62
    y2 = 80
    x1 = 85 + (70 * current) + offset
    x2 = x1 + 14
    characters[i] = (x1, y1, x2, y2)

# Extract the characters from the image
# For each character, a sub-image is created by cropping the original image
# The sub-image is then saved to a file
for character, coordinates in characters.items():
    x1, y1, x2, y2 = coordinates
    area = image.crop((x1, y1, x2, y2))
    area.save(f"imgs/{character}.png")