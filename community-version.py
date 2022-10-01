## Community Version
import sys

from math import ceil
from random import choice
from time import sleep

from PIL import Image


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert("L")


def map_pixels_to_ascii_chars(image, range_width):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [
        ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image
    ]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(
    image,
    range_width,
    new_width=100,
):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, range_width)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    return "\n".join(image_ascii)


def handle_image_print(image_ascii):
    verbs = [
        "Articulating",
        "Coordinating",
        "Gathering",
        "Powering up",
        "Clicking on",
        "Backing up",
        "Extrapolating",
        "Authenticating",
        "Recovering",
        "Finalizing",
        "Testing",
        "Upgrading",
    ]

    nouns = [
        "scope",
        "lunch",
        "meetings",
        "skeletons",
        "devices",
        "margins",
        "bookmarks",
        "CPUs",
        "folders",
        "emails",
        "disks",
        "JPEGs",
        "ROMs",
        "Viruses",
    ]

    print("Turning your image into ASCII art...")
    sleep(1)
    for i in range(4):
        print(f"{choice(verbs)} {choice(nouns)}...")
        sleep(1)
    print("Here we go...!")
    sleep(1)
    print()
    print(image_ascii)


def handle_image_conversion(image_filepath, range_width):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image, range_width=range_width)
    handle_image_print(image_ascii)


if __name__ == "__main__":
    if (
        len(sys.argv) == 3
    ):  # The user Specefied which CHAR_SET to use or included his/her own
        CHAR_SET = sys.argv[
            2
        ]  # Either an integer value specifying which previously made set to use, or a list value with the characters to use

        if CHAR_SET[0] == "[" and CHAR_SET[-1] == "]":  # is a list
            CHAR_SET = list(CHAR_SET.split(","))[1:-1]  # Convert the string into a list
            print(CHAR_SET)

        else:
            try:
                CHAR_SET = int(CHAR_SET)

            except:
                raise Exception(
                    "Please insert a correct value, either an int value to select which CHAR_SET to use, or a list value of characters of your own!"
                )

    else:  # If the user did not select a CHAR_SET
        CHAR_SET = 1  # Default CHAR_SET

    # Check if the CHAR_SET is a list value
    if isinstance(CHAR_SET, list):
        ASCII_CHARS = CHAR_SET
        range_width = ceil(
            (255 + 1) / len(ASCII_CHARS)
        )  # as the range width is based on the number of ASCII_CHARS we have

    elif isinstance(CHAR_SET, int):
        if CHAR_SET == 1:  # The original CHAR_SET from the example file
            ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
            range_width = 25

        elif CHAR_SET == 2:
            ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
            range_width = 32

        else:
            raise Exception("Sorry, there are no CHAR_SET of the value you selected")
    else:
        raise Exception("The value you choosed is neither an integer nor a list.")

    image_file_path = sys.argv[1]
    print(image_file_path)
    handle_image_conversion(image_file_path, range_width)
