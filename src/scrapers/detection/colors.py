import json
import numpy as np
from PIL import Image


def get_mean_color(key, img, top_left):
    """
    This function calculates the mean color of a 2x2 pixel area in an image.

    Args:
        key: The key representing the area in the image.
        img: A numpy array representing the image.
        top_left: A tuple representing the coordinates of the top left pixel of the area.

    Returns:
        A numpy array representing the mean color of the area.
    """
    print(f"Getting color for {key} at {top_left}")
    # Get the 2x2 pixel area from the image
    pixels = img[top_left[1]: top_left[1] + 2, top_left[0]: top_left[0] + 2]
    # Save the area as an image for debugging
    Image.fromarray(pixels).save(f"debug/{key}.png")

    # Calculate and return the mean color of the area
    return np.mean(pixels, axis=(0, 1))


def main():
    """
    This function is the main entry point of the program.

    It loads the areas from a JSON file, calculates the mean color of each area in each image in the "imgs" directory,
    and saves the calculated mean colors to a JSON file.
    """
    # Load the areas from the JSON file
    with open("areas.json", "r") as f:
        areas = json.load(f)

    # Initialize an empty dictionary to store the mean colors
    colors = {}

    # Iterate over each area
    for key in areas:
        # Load the image for the area as a numpy array
        img = np.array(Image.open(f"imgs/{key}.png"))
        # Calculate the mean color of the area and store it in the dictionary
        colors[key] = get_mean_color(key, img, areas[key]).tolist()

    # Save the mean colors to a JSON file
    with open("colors.json", "w") as f:
        json.dump(colors, f)


if __name__ == "__main__":
    main()
