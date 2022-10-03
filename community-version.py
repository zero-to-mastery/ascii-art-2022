# Community Version
import argparse

from math import ceil
from random import choice
from time import sleep

from PIL import Image, ImageChops
from rich.console import Console


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
    console = Console()
    with console.status("[bold green]Turning your image into ASCII art..."):
        for _ in range(4):
            console.log(f"{choice(verbs)} {choice(nouns)}...")
            sleep(1)
        sleep(1)

    console.log("[bold green]Here we go...!")
    print(image_ascii)


def inverse_image_color(image):
    inverted_image = ImageChops.invert(image)
    return inverted_image

# color of ascii characters
def ascii_color(image_filepath, range_width, col):
    console = Console()
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    img = convert_image_to_ascii(image, range_width)
    console.print(img, style=col)


def handle_image_conversion(image_filepath, range_width, inverse_color):
    image = None
    try:
        image = Image.open(image_filepath)
        if inverse_color:
            image = inverse_image_color(image)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image, range_width=range_width)
    handle_image_print(image_ascii)


def init_args_parser():
    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument(
        dest="image_file_path", nargs="?", type=str, help="Image file path."
    )
    parser.add_argument(
        dest="CHAR_SET",
        nargs="?",
        type=str,
        help="Input 1 or 2 to select pre-defined character sets."
        + "Or, input a list of characters in the format '[a,b,c,d]'.",
    )

    # flag arguments
    parser.add_argument(
        "--inverse", dest="inverse_image", action="store_true", default=False
    )
    parser.add_argument(
        "--color", dest="color_ascii", default=False, type = str,
        help="Add color to your ascii art by mentioning a color after --color." 
        + "For example, --color red produces ascii art of red in color."
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = init_args_parser()
    # The user Specified which CHAR_SET to use or included his/her own
    if args.CHAR_SET:
        # Either an integer value specifying which previously made set to use, or a list value with the characters to use
        CHAR_SET = args.CHAR_SET

        if CHAR_SET[0] == "[" and CHAR_SET[-1] == "]":  # is a list
            CHAR_SET = CHAR_SET[1:-1].split(",")  # Convert the string into a list
            print("Using custom character set:", CHAR_SET)
        else:
            try:
                CHAR_SET = int(CHAR_SET)

            except ValueError:
                raise ValueError(
                    "Please insert a correct value, either an int value to select which CHAR_SET to use, or a list value of characters of your own!"
                )

    else:  # If the user did not select a CHAR_SET
        CHAR_SET = 1  # Default CHAR_SET

    # Check if the CHAR_SET is a list value
    if isinstance(CHAR_SET, list):
        ASCII_CHARS = CHAR_SET
        # as the range width is based on the number of ASCII_CHARS we have
        range_width = ceil((255 + 1) / len(ASCII_CHARS))

    elif isinstance(CHAR_SET, int):
        if CHAR_SET == 1:  # The original CHAR_SET from the example file
            ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
            range_width = 25

        elif CHAR_SET == 2:
            ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
            range_width = 32

        else:
            raise Exception("Sorry, there are no CHAR_SET of the value you selected.")
    else:
        raise Exception("The value you chose is neither an integer nor a list.")

    image_file_path = args.image_file_path

    if not image_file_path:
        image_file_path = input("Oops, you forgot to specify an Image path: ")

    print(image_file_path)
    handle_image_conversion(image_file_path, range_width, args.inverse_image)

    # ascii color
    ascii_color(image_file_path, range_width, args.color_ascii)
    # handle_image_conversion(image_file_path, range_width, args.inverse_image)
