import os
import sys
from PIL import Image
from tkinter import END, RAISED, Button, Frame, Label, Scrollbar, Text, Tk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as ms

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from community_version import convert_image_to_ascii


W_WIDTH = 1200
W_HEIGHT = 680
FILES_IMG_EXTENSION = [
    ("All Images", "*.jpg;*.jpeg;*.png"),
    ("JPEG", "*.jpg"),
    ("JPEG", "*.jpeg"),
    ("PNG", "*.png"),
]
RANGE_WIDTH = 25
ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]


def open_file():
    """open file in File Explorer"""

    filepath = askopenfilename(filetypes=FILES_IMG_EXTENSION)

    if not filepath:
        return

    txt_ascii_art.config(state="normal")
    txt_ascii_art.delete("1.0", END)
    img = Image.open(filepath)
    ascii_art = convert_image_to_ascii(img, RANGE_WIDTH, ascii_chars=ASCII_CHARS)
    txt_ascii_art.insert(END, ascii_art)
    txt_ascii_art.config(state="disabled")
    filename = filepath.split("/")[-1]
    window.title(f"Image to ASCII converter - {filename}")


def save_file():
    ms.showerror("Error", "functionality not implemented yet")
    pass


def init_window() -> Tk:
    window = Tk()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (W_WIDTH / 2))
    y_cordinate = int((screen_height / 2) - (W_HEIGHT / 2) - 50)
    window.geometry(f"{W_WIDTH}x{W_HEIGHT}+{x_cordinate}+{y_cordinate}")
    window.title("Image to ASCII converter")
    # Currently not allow to resize the window
    window.resizable(False, False)
    return window


window = init_window()


# Label(
#     window,
#     text="Image to ASCII Convertor",
#     fg="black",
#     font=("Times", 25, "bold"),
#     width=25,
# )

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_ascii_art = Text(window, state="disabled")
frm_buttons = Frame(window, relief=RAISED, bd=2)
btn_open = Button(window, text="Open", command=open_file)
btn_save = Button(frm_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_ascii_art.grid(row=0, column=1, sticky="nsew")

window.mainloop()
