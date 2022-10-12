from math import ceil
import os
import time
import json

# https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
########################################
from flask import Flask, request, redirect, render_template
from PIL import Image
from werkzeug.utils import secure_filename
from community_version import convert_image_to_ascii
from pathlib import Path
from colorama import Fore, Back, Style
from constants import ASCII_CHARS

IMG_FOLDER = os.path.join("static", "IMG")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * \
    1024  # File can not be largr than 16 Mb
app.config["UPLOAD_FOLDER"] = IMG_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_for_folder():
    """Basically it will check if there are already existing folder named images or not"""
    if not Path.cwd().name == "webapp":
        print(
            f"{Fore.RED}Please shift to webapp directory for program to run properly. {Back.WHITE}'cd webapp'{Style.RESET_ALL}"
        )
        quit()  # Just quit the file because that makes things easier and less complex
    # If this if block is not supplied then python will create the IMG_FOLDER directory outside and cause conflictions.
    if Path.cwd().name == "webapp":
        if os.path.isdir("static"):
            return print(f"{Fore.GREEN}Existing Directories Found.{Style.RESET_ALL}")
        for dirs in [IMG_FOLDER]:
            if not os.path.isdir(dirs):
                os.makedirs(dirs, mode=777)
            print(f"{Fore.YELLOW}Initializig Directories...{Style.RESET_ALL}")


check_for_folder()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", template_name='home')

@app.route("/generate", methods=["POST"])
def generate_art():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect('/')

        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return render_template(
                "home.html",
                file_error="There is an error about the filename or have not passed the file. Please try again!",
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
        
        # redirect to gallery page
        return redirect(f'/gallery/{filename}')

        
@app.route("/gallery/<string:filename>", methods=["GET"])
@app.route("/gallery/", methods=["GET"])
@app.route("/gallery", methods=["GET"])
def show_art_or_gallery(filename=None):
    if filename is not None:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
        img = Image.open(filepath)

        ascii_chars = ["#", "?", "%", ".",
                        "S", "+", ".", "*", ":", ",", "@"]
        range_width = 25
        ascii_art = convert_image_to_ascii(
            img, ascii_chars, range_width, fix_aspect_ratio=True
        )

        return render_template("art.html", ascii_art=ascii_art, template_name="art")
    else:
        images = [x for x in os.listdir("static/IMG") if allowed_file(x)]
        return render_template("gallery.html", images=images, template_name="gallery")


@app.route("/delete", methods=["POST"])
def delete_file():
    if request.method == "POST":
        filename = request.form.get("filename")
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.remove(filepath)
        return redirect("/gallery")

if __name__ == "__main__":
    app.run(debug=True)
