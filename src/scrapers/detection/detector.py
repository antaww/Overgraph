import json
import os

import numpy as np
from PIL import Image

def get_mean_color(img, top_left):
    # get the area
    pixels = img[top_left[1]: top_left[1] + 2, top_left[0]: top_left[0] + 2]

    # get the mean of the colors
    return np.mean(pixels, axis=(0, 1))


def get_closest_color(colors_json, colors_scanned):
    def distance_rgb(couleur1, couleur2):
        return sum((x - y) ** 2 for x, y in zip(couleur1, couleur2)) ** 0.5

    min_distance = float('inf')
    closest_key = None

    for key in colors_json:
        if key in colors_scanned:
            distance = distance_rgb(colors_json[key], colors_scanned[key])
            if distance < min_distance:
                min_distance = distance
                closest_key = key

    return closest_key


def main():
    # load the areas
    with open("areas.json", "r") as f:
        areas = json.load(f)

    # load the colors
    with open("colors.json", "r") as f:
        colors_json = json.load(f)

    colors = {}

    # load the image with every key from areas
    for image in os.listdir("tests"):
        if image.endswith(".png"):
            img = np.array(Image.open(f"tests/{image}"))
            for key in areas:
                colors[key] = get_mean_color(img, areas[key]).tolist()
            print(f"{image} >> {colors}")

            closest = get_closest_color(colors_json, colors)
            colors = {}
            print(f"closest for {image} >> {closest}")


if __name__ == "__main__":
    main()
