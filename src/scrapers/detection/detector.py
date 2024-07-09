import json
import os

import numpy as np
from PIL import Image


def get_mean_color(img, top_left):
    """
    This function calculates the mean color of a 2x2 pixel area in an image.

    Args:
        img: A numpy array representing the image.
        top_left: A tuple representing the coordinates of the top left pixel of the area.

    Returns:
        A numpy array representing the mean color of the area.
    """
    # Get the 2x2 pixel area from the image
    pixels = img[top_left[1]: top_left[1] + 2, top_left[0]: top_left[0] + 2]

    # Calculate and return the mean color of the area
    return np.mean(pixels, axis=(0, 1))


def get_closest_color(colors_json, colors_scanned):
    """
    This function finds the color in colors_json that is closest to any color in colors_scanned.

    Args:
        colors_json: A dictionary where the keys are color names and the values are RGB color values.
        colors_scanned: A dictionary where the keys are color names and the values are RGB color values.

    Returns:
        The name of the color in colors_json that is closest to any color in colors_scanned.
    """

    def distance_rgb(couleur1, couleur2):
        """
        This function calculates the Euclidean distance between two colors.

        Args:
            couleur1: The first color as an RGB tuple.
            couleur2: The second color as an RGB tuple.

        Returns:
            The Euclidean distance between the two colors.
        """
        return sum((x - y) ** 2 for x, y in zip(couleur1, couleur2)) ** 0.5

    min_distance = float('inf')
    closest_key = None

    # Iterate over each color in colors_json
    for key in colors_json:
        # If the color is also in colors_scanned
        if key in colors_scanned:
            # Calculate the distance between the two colors
            distance = distance_rgb(colors_json[key], colors_scanned[key])
            # If the distance is less than the current minimum distance
            if distance < min_distance:
                # Update the minimum distance and the closest color
                min_distance = distance
                closest_key = key

    # Return the closest color
    return closest_key


def main():
    """
    This function is the main entry point of the program.

    It loads the areas and colors from JSON files, calculates the mean color of each area in each image in the "tests"
    directory, and finds the color in the colors JSON file that is closest to each calculated mean color.
    """
    # Load the areas from the JSON file
    with open("areas.json", "r") as f:
        areas = json.load(f)

    # Load the colors from the JSON file
    with open("colors.json", "r") as f:
        colors_json = json.load(f)

    colors = {}

    # Iterate over each image in the "tests" directory
    for image in os.listdir("tests"):
        if image.endswith(".png"):
            # Load the image as a numpy array
            img = np.array(Image.open(f"tests/{image}"))
            # Calculate the mean color of each area in the image
            for key in areas:
                colors[key] = get_mean_color(img, areas[key]).tolist()
            print(f"{image} >> {colors}")

            # Find the color in the colors JSON file that is closest to each calculated mean color
            closest = get_closest_color(colors_json, colors)
            colors = {}
            print(f"closest for {image} >> {closest}")


if __name__ == "__main__":
    main()
