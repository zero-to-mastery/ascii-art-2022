# Community Version
import argparse
import webbrowser

from math import ceil
from pathlib import Path
from random import choice
from time import sleep
from sys import stdin
from io import BytesIO

from PIL import Image, ImageChops
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from rich.console import Console


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio / 2 * new_width)

    new_image = image.resize((new_width, new_height))
    # Small size image won't be look good do creating images with minimum 500*500
    if CHAR_SET == 3:
        new_width = 500
        new_height = 500
        new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert("L")


def map_pixels_to_color(image, range_width, color, new_width=500, new_height=500):
    b = (0, 0, 0)
    y = (255, 255, 0)
    # creating new image with two different colors. Mixing more colors makes image blur.
    ASCII_CHARS = [b, y, b, y]

    image = scale_image(image)
    image = convert_to_grayscale(image)
    pixels_in_image = list(image.getdata())

    pixels_to_chars = [
        ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image
    ]
    # creating matrix to write new image with colors
    arr_2d = []
    arr3 = []
    temp = 0
    for j in range(0, new_height):
        start_value = temp
        end_value = new_width * (j + 1)
        for i in range(start_value, end_value):
            arr3.append(pixels_to_chars[i])
        # print(arr_2d)
        arr_2d.append(arr3)
        arr3 = []
        temp = end_value
    # Re-writing  pixel
    smiley = Image.new("RGB", (new_width, new_height))
    for row in range(500):
        for col in range(new_width):
            smiley.putpixel((col, row), arr_2d[row][col])
            # smiley.save('test.jpg')
    return smiley.show()


def map_pixels_to_ascii_chars(image, range_width, ASCII_CHARS):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """
    # set default ascii character list
    if ASCII_CHARS == None:
        ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [
        ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image
    ]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(
    image, range_width, new_width=100, ASCII_CHARS=None, fix_aspect_ratio=False
):
    # set default ascii character list
    if ASCII_CHARS == None:
        ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, range_width, ASCII_CHARS)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    if fix_aspect_ratio:
        # The generated ascii image is approximately 1.35 times
        # larger than the original image
        # So, we will drop one line after every 3 lines
        image_ascii = [char for index, char in enumerate(image_ascii) if index % 4 != 0]

    return "\n".join(image_ascii)


def handle_image_print(image_ascii, color, store):
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

    # To print beautiful dummy progress bar to the user
    with console.status("[bold green]Turning your image into ASCII art..."):
        for _ in range(4):
            console.log(f"{choice(verbs)} {choice(nouns)}...")
            sleep(1)
        sleep(1)

        # print the ASCII art to the console.
        console.log("[bold green]Here we go...!")
        if CHAR_SET == 3:
            map_pixels_to_color(image, range_width=range_width, color=args.color_ascii)
        else:
            if color:
                console.print(image_ascii, style=color)
            else:
                console.print(image_ascii)


def inverse_image_color(image):
    inverted_image = ImageChops.invert(image)
    return inverted_image


def handle_image_conversion(image: Image, range_width, inverse_color, color=None):
    if inverse_color:
        image = inverse_image_color(image)

    image_ascii = convert_image_to_ascii(
        image, range_width=range_width, ASCII_CHARS=ASCII_CHARS
    )
    return image_ascii, color


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
        help=(
            "Input 1 or 2 to select pre-defined character sets, 3 for a yellow-black image, "
            "or input a list of characters in the format '[a,b,c,d]'."
        ),
    )

    # flag arguments
    parser.add_argument(
        "--inverse", dest="inverse_image", action="store_true", default=False
    )
    parser.add_argument(
        "--color",
        dest="color_ascii",
        type=str,
        help=(
            "Add color to your ascii art by mentioning a color after --color. "
            "For example, --color red produces ascii art of red in color. "
            "It also supports hash code that can help you to choose more colors."
        ),
    )
    parser.add_argument(
        "--store",
        dest="store_art",
        type=Path,
        help=(
            "Save the ASCII art of the image to a given path. E.g., --store output.svg. "
            "The result will be great if you choose a svg file extension."
        ),
    )
    parser.add_argument(
        dest="stdin",
        nargs="?",
        type=argparse.FileType("rb"),
        help="Read image from stdin",
        default=stdin,
    )

    args = parser.parse_args()

    return args


def store_ascii_art():
    pass


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
                    "Please insert a correct value, "
                    "either an int value to select which CHAR_SET to use, "
                    "or a list value of characters of your own!"
                )

    else:  # If the user did not select a CHAR_SET
        CHAR_SET = 1  # Default CHAR_SET

    # Check if the CHAR_SET is a list value
    if isinstance(CHAR_SET, list):
        ASCII_CHARS = CHAR_SET

    elif isinstance(CHAR_SET, int):
        if CHAR_SET == 1:  # The original CHAR_SET from the example file
            ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

        elif CHAR_SET == 2:
            ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]

        elif CHAR_SET == 3:
            ASCII_CHARS = ["b", "w", "b"]

        else:
            raise Exception("Sorry, there are no CHAR_SET of the value you selected.")
    else:
        raise Exception("The value you chose is neither an integer nor a list.")

    # as the range width is based on the number of ASCII_CHARS we have
    range_width = ceil((255 + 1) / len(ASCII_CHARS))

    image = None
    is_stdin = not args.stdin.isatty()

    if is_stdin:
        buffer = args.stdin.buffer.read()
        image = Image.open(BytesIO(buffer))
    else:
        image_file_path = args.image_file_path
        if not image_file_path:
            completer = PathCompleter()
            image_file_path = prompt(
                "Oops, you forgot to specify an Image path: ", completer=completer
            )

        if image_file_path:
            print(image_file_path)
            try:
                image = Image.open(image_file_path)
            except Exception as e:
                print(f"Unable to open image file {image_file_path}.")
                print(e)
                exit(1)

    if not image:
        raise Exception("No image was loaded")

    # convert the image to ASCII art
    if CHAR_SET == 3:
        capture = handle_image_print(
            image, color=args.color_ascii, store=args.store_art
        )
        # map_pixels_to_color(image, range_width=range_width, color=args.color_ascii)
    else:
        image_ascii, color = handle_image_conversion(
            image, range_width, args.inverse_image, args.color_ascii
        )
        # display the ASCII art to the console
        capture = handle_image_print(image_ascii, color, args.store_art)

    ### Save the image ###
    if args.store_art:

        try:
            if args.store_art.suffix in (".txt", ".svg"):
                with open(args.store_art, "wt") as report_file:
                    console = Console(style=color, file=report_file, record=True)
                    if args.store_art.suffix == ".svg":
                        if color:
                            console.print(image_ascii, style=color)
                            console.save_svg(
                                args.store_art, title="ASCII_conversion_Of_Image.py"
                            )
                            webbrowser.open(
                                f"file://{args.store_art.absolute()}", new=1
                            )
                        else:
                            console.print(image_ascii)
                    else:
                        if color:
                            console.print(image_ascii, style=color)
                        else:
                            console.print(image_ascii)
            else:
                raise Exception("The file extension did not match as txt file!")
        except Exception as e:
            print(e)
            print(
                "\33[101mOops, I think you have choosed wrong file extension. Please give a svg file name e.g., output.txt \033[0m"
            )
