import json
import os

import cv2
import numpy as np
from PIL import Image

# load image
image = Image.open("frame.jpg")

# get the size of the image
width, height = image.size
print("Dimensions de l'image:", width, "x", height)

characters = {}

# Define the coordinates of the characters
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

# Extract the characters
for character, coordinates in characters.items():
    x1, y1, x2, y2 = coordinates
    zone_extraite = image.crop((x1, y1, x2, y2))
    zone_extraite.save(f"test_icons/{character}.png")