import json

import numpy as np
from PIL import Image


def get_mean_color(key, img, top_left):
    print(f"Getting color for {key} at {top_left}")
    # get the area
    pixels = img[top_left[1]: top_left[1] + 2, top_left[0]: top_left[0] + 2]
    # save image for debug
    Image.fromarray(pixels).save(f"debug/{key}.png")

    # get the mean of the colors
    return np.mean(pixels, axis=(0, 1))


def main():
    # load the areas
    with open("areas.json", "r") as f:
        areas = json.load(f)

    # create a dictionary to store the colors
    colors = {}
    # load the image with every key from areas
    for key in areas:
        img = np.array(Image.open(f"imgs/{key}.png"))
        colors[key] = get_mean_color(key, img, areas[key]).tolist()

    # save the colors
    with open("colors.json", "w") as f:
        json.dump(colors, f)


if __name__ == "__main__":
    main()
