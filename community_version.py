# Community Version
import argparse
import webbrowser
import re

from math import ceil
from pathlib import Path
from random import choice
from time import sleep
from sys import stdin
from io import BytesIO

from PIL import Image, ImageChops, UnidentifiedImageError
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from rich.console import Console


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio / 2 * new_width)
    return image.resize((new_width, new_height))


def convert_to_grayscale(image):
    return image.convert("L")


def map_pixels_to_color(image, new_width=500, new_height=500):
    b = (0, 0, 0)
    y = (255, 255, 0)
    # creating new image with two different colors. Mixing more colors makes image blur.
    ASCII_CHARS = [b, y, b, y]

    image = image.resize((new_width, new_height))
    image = convert_to_grayscale(image)
    pixels_in_image = list(image.getdata())

    pixels_to_chars = [
        ASCII_CHARS[int(pixel_value / 86)] for pixel_value in pixels_in_image
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
        arr_2d.append(arr3)
        arr3 = []
        temp = end_value
    # Re-writing  pixel
    smiley = Image.new("RGB", (new_width, new_height))
    for row in range(500):
        for col in range(new_width):
            smiley.putpixel((col, row), arr_2d[row][col])
    return smiley.show()


def map_pixels_to_ascii_chars(image, range_width, ascii_chars):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [
        ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image
    ]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(
    image,
    ascii_chars,
    range_width,
    new_width=100,
    fix_aspect_ratio=False,
):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, range_width, ascii_chars)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    if fix_aspect_ratio:
        # The generated ASCII image is approximately 1.35 times
        # larger than the original image
        # So, we will drop one line after every 3 lines
        image_ascii = [char for index, char in enumerate(image_ascii) if index % 4 != 0]

    return "\n".join(image_ascii)

def single_ascii_replacement(image_ascii,singleAsciiChar):
    #Creating list for ASCII character and their count
    asc_count = []
    for asc_char in ["%","?","+","°","@","O","o","#","."":",",","*"," "]:
        asc_count.append((asc_char , image_ascii.count(asc_char)))
    asc_count.sort(key = lambda x:x[1] ,reverse=True)
    chr=asc_count[0][0]
    
    #Replacing highest ASCII character with blank
    new_image_re = re.sub(rf"{chr}", " ", image_ascii)
    #Replacing ASCII characters with given single character
    new_image = re.sub(r"[!S%?+°@Oo#.:,*]", singleAsciiChar, new_image_re)
    image_ascii = new_image
    return image_ascii


def hype(console):
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

    # To print beautiful dummy progress bar to the user
    with console.status("[bold green]Turning your image into ASCII art..."):
        for _ in range(4):
            console.log(f"{choice(verbs)} {choice(nouns)}...")
            sleep(1)
        sleep(1)
    console.log("[bold green]Here we go...!")

def welcome_message(console):
    console.print("[bold yellow] Welcome to ASCII ART Generator!")

def handle_black_yellow(image):
    map_pixels_to_color(image)

def handle_image_print(image_ascii, color=None):
    console = Console()

    welcome_message(console)

    hype(console)

    # print the ASCII art to the console.
    if color:
        console.print(image_ascii, style=color)
    else:
        console.print(image_ascii)


def inverse_image_color(image):
    return ImageChops.invert(image)


def handle_image_conversion(image, range_width, ascii_chars, inverse_color):
    if inverse_color:
        image = inverse_image_color(image)

    image_ascii = convert_image_to_ascii(
        image, range_width=range_width, ascii_chars=ascii_chars
    )

    return image_ascii


def init_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        dest="image_file_path", nargs="?", type=str, help="Image file path."
    )

    parser.add_argument(
        dest="stdin",
        nargs="?",
        type=argparse.FileType("rb"),
        help="Read image from stdin",
        default=stdin,
    )

    parser.add_argument(
        "--preset",
        dest="preset",
        type=int,
        choices=[1, 2],
        help="Select 1 or 2 for predefined ASCII character sets.",
    )

    parser.add_argument(
        "--charset",
        dest="charset",
        nargs="+",
        help="A list of characters to display the image, from darkest to brightest.",
    )

    parser.add_argument(
        "--black-yellow",
        dest="black_yellow",
        action="store_true",
        help="Output a black and yellow image. Does not work if a character set was already chosen.",
    )

    parser.add_argument(
        "--inverse", dest="inverse_image", action="store_true", default=False
    )

    parser.add_argument(
        "--color",
        dest="color",
        type=str,
        help=(
            "Add color to your ASCII art by mentioning a color after --color. "
            "It also supports hexadecimal notation that can help you to choose more colors."
        ),
    )

    parser.add_argument(
        "--store",
        dest="store_art",
        type=Path,
        help=(
            "Save the ASCII art of the image to a given path, e.g., --store output.txt. "
            "The result will be great if you choose a .svg file extension."
        ),
    )

    parser.add_argument(
        "--singleAsciiChar",
        dest="singleAsciiChar",
        type=str,
        help="A single ASCII character  to display the image. "
        "It usages existing default preset character to convert it into single.",
    )

    return parser.parse_args()


def get_predefined_charset(preset=1):
    if preset == 1:
        return [" ", ".", "°", "*", "o", "O", "#", "@"]
    if preset == 2:
        return ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
    raise ValueError("Preset character sets are either 1 or 2.")


def read_image_from_stdin(buffer):
    buffer = buffer.read()
    return Image.open(BytesIO(buffer))


def ask_user_for_image_path_until_success(get_image):
    image = None
    while True:
        try:
            image = get_image()
        except FileNotFoundError:
            print("The specified path does not exist, please try again.")
            return ask_user_for_image_path_until_success(
                lambda: Image.open(prompt("> ", completer=PathCompleter()))
            )
        except UnidentifiedImageError:
            print("The specified path is not of a valid image, please try again.")
            return ask_user_for_image_path_until_success(
                lambda: Image.open(prompt("> ", completer=PathCompleter()))
            )
        else:
            return image


def read_image_from_path(path=None):
    if path:
        return ask_user_for_image_path_until_success(lambda: Image.open(path))
    else:
        print(
            "No path specified as argument, please type a path to an image or Ctrl-C to quit."
        )
        return ask_user_for_image_path_until_success(
            lambda: Image.open(prompt("> ", completer=PathCompleter()))
        )


def handle_store_art(path, image_ascii, color):
    try:
        if path.suffix in (".txt", ".svg"):
            with open(path, "wt") as report_file:
                console = Console(style=color, file=report_file, record=True)
                if path.suffix == ".svg":
                    if color:
                        console.print(image_ascii, style=color)
                        console.save_svg(path, title="ZTM ASCII Art 2022")
                        webbrowser.open(f"file://{path.absolute()}", new=1)
                elif color:
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


def main():
    args = init_args_parser()

    if not args.stdin.isatty():
        image = read_image_from_stdin(args.stdin.buffer)
    else:
        image = read_image_from_path(args.image_file_path)

    if args.preset:
        ascii_chars = get_predefined_charset(args.preset)
    elif args.charset:
        print(f"Using custom character set: {', '.join(args.charset)}")
        ascii_chars = args.charset
    else:
        ascii_chars = get_predefined_charset()

    # as the range width is based on the number of ASCII_CHARS we have
    range_width = ceil((255 + 1) / len(ascii_chars))

    # convert the image to ASCII art
    if args.black_yellow:
        handle_black_yellow(image)
        return

    image_ascii = handle_image_conversion(
        image, range_width, ascii_chars, args.inverse_image
    )
    if args.singleAsciiChar:
        image_ascii = single_ascii_replacement(image_ascii,args.singleAsciiChar)

    # display the ASCII art to the console
    handle_image_print(image_ascii, args.color)

    ### Save the image ###
    if args.store_art:
        handle_store_art(args.store_art, image_ascii, args.color)


if __name__ == "__main__":
    main()
