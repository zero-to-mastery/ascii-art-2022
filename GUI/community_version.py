# Community Version
import argparse
import pyfiglet

import tkinter.messagebox as ms
from tkinter import *
from tkinter.filedialog import askopenfilename

import tkinter as tk
from tkinter import ttk

from math import ceil
from random import choice
from time import sleep

from PIL import Image, ImageChops
from rich.console import Console

FILES_IMG_EXTENSION = [
    ("All Images", "*.jpg;*.jpeg;*.png"),
    ("JPEG", "*.jpg"),
    ("JPEG", "*.jpeg"),
    ("PNG", "*.png"),
]


class ImageProcessor:
    @staticmethod
    def scale_image(image, new_width=100):
        """Resizes an image preserving the aspect ratio."""
        (original_width, original_height) = image.size
        aspect_ratio = original_height / float(original_width)
        new_height = int(aspect_ratio / 2 * new_width)

        new_image = image.resize((new_width, new_height))
        return new_image

    @staticmethod
    def convert_to_grayscale(image):
        return image.convert("L")

    @staticmethod
    def inverse_image_color(image):
        inverted_image = ImageChops.invert(image)
        return inverted_image

    @staticmethod
    def process_image(image_filepath, inverse_color):
        image = None
        try:
            image = Image.open(image_filepath)
            if inverse_color:
                image = ImageProcessor.inverse_image_color(image)
        except IOError as e:
            ms.showerror("Oops", f"Unable to open image file.")
            app.destroy()
            exit()
        return image


class Image2ASCIIConverter:
    def __init__(self, ASCII_Chars=None):
        if ASCII_Chars is None:
            ASCII_Chars = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
        self.ASCII_Chars = ASCII_Chars

    def map_pixels_to_ascii_chars(self, image, range_width):
        """Maps each pixel to an ascii char based on the range
        in which it lies.
        0-255 is divided into 11 ranges of 25 pixels each.
        """
        pixels_in_image = list(image.getdata())
        pixels_to_chars = [
            self.ASCII_Chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image
        ]
        return "".join(pixels_to_chars)

    def convert_image_to_ascii(
            self,
            image,
            range_width,
            new_width=100,
    ):
        image = ImageProcessor.scale_image(image)
        image = ImageProcessor.convert_to_grayscale(image)

        pixels_to_chars = self.map_pixels_to_ascii_chars(image, range_width)
        len_pixels_to_chars = len(pixels_to_chars)

        image_ascii = [
            pixels_to_chars[index: index + new_width]
            for index in range(0, len_pixels_to_chars, new_width)
        ]

        return "\n".join(image_ascii)

    def handle_image_conversion(self, image, range_width):
        image_ascii = self.convert_image_to_ascii(image, range_width=range_width)
        return image_ascii


class OutputWriter:
    def __init__(self, color, outputs=None):
        if outputs is None:
            outputs = ["console"]
        self.outputs = outputs
        self.color = color
        self.verbs = [
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

        self.nouns = [
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

    def print_prepare_info(self):

        console = Console()

        # To print beautiful dummy progress bar to the user
        with console.status("[bold green]Turning your image into ASCII art..."):
            for _ in range(4):
                console.log(f"{choice(self.verbs)} {choice(self.nouns)}...")
                sleep(1)
            sleep(1)
            console.print("[bold green]Here we go...!")

    def get_out_paths(self):
        out_paths = []
        for out in self.outputs:
            if out[-4:] == ".txt":
                out_paths.append(out)
        return out_paths

    def write(self, ASCII_image):
        if 'console' in self.outputs:
            self.print_prepare_info()
            print(ASCII_image)
        out_paths = self.get_out_paths()
        if len(out_paths) != 0:
            for out in out_paths:
                OutputWriter.write_to_txtfile(ASCII_image, out)

    @staticmethod
    def write_to_txtfile(content, filename="output.txt"):
        try:
            with open(filename, "w") as text_file:
                text_file.write(content)
                app.destroy()
                ms.showinfo("Success", "Image converted to ASCII Art ! Check output.txt !")
        except IOError:
            ms.showinfo("Failure", "We couldn't write ASCIIfied image the output file!")


class Utilities:

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()

        # positional arguments
        parser.add_argument(
            dest="CHAR_SET",
            nargs="?",
            type=str,
            help=(
                "Input 1 or 2 to select pre-defined character sets. "
                "Or, input a list of characters in the format '[a,b,c,d]'."
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
            default=None,
            help=(
                "Add color to your ascii art by mentioning a color after --color. "
                "For example, --color red produces ascii art of red in color. "
                "It also supports hash code that can help you to choose more colors."
            ),
        )
        parser.add_argument(
            "--store",
            dest="store_art",
            default=None,
            type=str,
            help=(
                "Save the ASCII art of the image to a given path. E.g., --store output.svg. "
                "The result will be great if you choose a svg file extension."
            )
        )

        args = parser.parse_args()

        return args

    @staticmethod
    def parse_charset(CHAR_SET):
        if CHAR_SET is None:
            CHAR_SET = "1"
        # Either an integer value specifying which previously made set to use, or a list value with the characters to use
        if type(CHAR_SET) == list and CHAR_SET[0] == "[" and CHAR_SET[-1] == "]":  # is a list
            ASCII_CHARS = CHAR_SET[1:-1].split(",")  # Convert the string into a list
            print("Using custom character set:", CHAR_SET)
            range_width = ceil((255 + 1) / len(CHAR_SET))
        elif type(CHAR_SET) in [int, str]:
            CHAR_SET = int(CHAR_SET)
            if CHAR_SET == 1:  # The original CHAR_SET from the example file
                ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
                range_width = 25

            elif CHAR_SET == 2:
                ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
                range_width = 32
            else:
                raise Exception("Sorry, there are no CHAR_SET of the value you selected.")
        else:
            raise ValueError(
                "Please insert a correct value, "
                "either an int value to select which CHAR_SET to use, "
                "or a list value of characters of your own!"
            )
        return ASCII_CHARS, range_width


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image to ASCII converter')
        self.geometry('800x220')
        ttk.Label(self, text="Image to ASCII Convertor", font=("Times", 25, "bold"), width=25).pack()

        self.btn_open = Button(self, text="Open", command=self.open_file)
        self.btn_open.place(x=80, y=60)

        self.label_image_path_status = Label(self, text="", font=(15))
        self.label_image_path_status.place(x=140, y=60)

        self.img_path_entry = Entry(self, bd=5, font=(15), width=70)
        self.img_path_entry.bind(self.main)
        self.img_path_entry.place(x=80, y=100)

        self.btn_convert = Button(self, text="Convert", font=("Times", 20), width=10, padx=5, pady=5, command=self.main)
        self.btn_convert.place(x=310, y=150)

        self.args = Utilities.get_args()
        self.ASCII_CHARS, self.range_width = Utilities.parse_charset(self.args.CHAR_SET)

    def main(self):
        image_file_path = self.img_path_entry.get()
        if not image_file_path:
            self.label_image_path_status["text"] = "Oops, you forgot to specify an Image path: "
            return
        print(pyfiglet.figlet_format("Welcome to ASCII ART Generator"))
        ascii_img = self.handle_image(image_file_path)
        ow = OutputWriter(self.args.color_ascii, self.args.store_art)
        ow.write(ascii_img)

    def open_file(self):
        filepath = askopenfilename(filetypes=FILES_IMG_EXTENSION)

        if not filepath:
            self.label_image_path_status["text"] = "Oops, you forgot to specify an Image path: "
            return

        self.img_path_entry.insert(0, filepath)
        self.label_image_path_status["text"] = "image is ready to convert"

    def handle_image(self, image_file_path):
        img_2_ascii_conv = Image2ASCIIConverter(self.ASCII_CHARS)

        image = ImageProcessor.process_image(image_file_path, self.args.inverse_image)

        image_ascii = img_2_ascii_conv.handle_image_conversion(
            image, self.range_width
        )
        return image_ascii


if __name__ == "__main__":
    app = App()
    app.mainloop()
