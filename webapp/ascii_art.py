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
from pyfiglet import Figlet, FigletFont

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

#################
#### App v1 #####
#################
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return render_template(
                "upload.html",
                file_error="There is an error about the filename or have not passed the file. Please try again!",
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img = Image.open(filepath)

            ascii_chars = ["#", "?", "%", ".",
                           "S", "+", ".", "*", ":", ",", "@"]
            range_width = 25
            ascii_ = convert_image_to_ascii(
                img, ascii_chars, range_width, fix_aspect_ratio=True
            )
            file.close()

            try:
                return render_template("ascii.html", ascii=ascii_)
            except Exception as e:
                return render_template(
                    "upload.html", error="Some error occurred! Try again"
                )

    return render_template("upload.html")


@app.route("/gallery/<path:file_path>", methods=["GET", "POST"])
def gallery(file_path=""):
    print(request.path)

    if request.form.get("char_set"):
        CHAR_SET = json.loads(request.form.get("char_set"))
    else:
        # use 1 as default if char_set is None
        CHAR_SET = ASCII_CHARS[1]

    IMG_LIST = os.listdir("static/IMG")
    IMG_LIST = ["IMG/" + i for i in IMG_LIST if allowed_file(i)]

    # lagging backslash is handled differently by different browsers
    if file_path != "main" and file_path != "main/":
        file = file_path
        filename = secure_filename(file.split("/")[-1])
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        img = Image.open(filepath)
        range_width = ceil((255 + 1) / len(CHAR_SET))
        ascii_ = convert_image_to_ascii(
            img, CHAR_SET, range_width, fix_aspect_ratio=True
        )
        return render_template("ascii_2.html", ascii=ascii_)

    return render_template("gallery.html", imagelist=IMG_LIST)


# lagging backslash is handled differently by different browsers
@app.route("/gallery/main/", methods=["POST"])
@app.route("/gallery/main", methods=["POST"])
def remove_file():
    for file in request.form:
        os.remove(os.path.join("static", file))
    IMG_LIST = os.listdir("static/IMG")

    IMG_LIST = ["IMG/" + i for i in IMG_LIST if allowed_file(i)]
    return render_template("gallery.html", imagelist=IMG_LIST)


@app.route("/toggle_darkmode", methods=["GET"])
def toggle_darkmode():
    # If Cookie does not exist, set to False before continuing
    if request.cookies.get("darkmode") == None:
        current_state = "False"
    else:
        current_state = request.cookies.get("darkmode")

    # Toggle string values
    current_state = "True" if current_state == "False" else "False"

    response = app.make_response("There should be a cookie")
    response.set_cookie("darkmode", current_state)
    return response


#################
#### App v2 #####
#################

@app.route("/v2", methods=["GET"])
def home():
    return render_template("home-v2.html", template_name='home')


@app.route("/v2/generate", methods=["POST"])
def generate_art():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect('/v2')

        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return render_template(
                "home-v2.html",
                file_error="There is an error about the filename or have not passed the file. Please try again!",
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

        # redirect to gallery page
        return redirect(f'/v2/gallery/{filename}')


@app.route("/v2/gallery/<string:filename>", methods=["GET"])
@app.route("/v2/gallery/", methods=["GET"])
@app.route("/v2/gallery", methods=["GET"])
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

        return render_template("art-v2.html", ascii_art=ascii_art, template_name="art")
    else:
        images = [x for x in os.listdir("static/IMG") if allowed_file(x)]
        return render_template("gallery-v2.html", images=images, template_name="gallery")


@app.route("/v2/delete", methods=["POST"])
def delete_file():
    if request.method == "POST":
        filename = request.form.get("filename")
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.remove(filepath)
        return redirect("/v2/gallery")


########################
#### Text ASCII Art ####
########################

@app.route("/v2/text", methods=["GET"])
def text_art():
    text_art = Figlet(font="standard").renderText("Zero to Mastery!")
    fonts = ['standard', 'slant', '3-d', '5lineoblique', '6x10', 'acrobatic', 'arrows', 'ascii___',
            'avatar', 'banner', 'banner3-D', 'banner3', 'banner4', 'big', 'block',
            'broadway', 'bubble', 'caligraphy', 'doh', 'doom', 'isometric1', 'isometric3',
            'nancyj-underlined', 'smkeyboard', 'univers']

    return render_template("text-art-v2.html", template_name='text', text_art=text_art, fonts=fonts)

@app.route("/v2/text/generate", methods=["POST"])
def generate_text_art():
    if request.method == "POST":
        text = request.form.get("text") or "Zero to Mastery!"
        font = request.form.get("font") or "slant"

        art = Figlet(font=font).renderText(text)
        
        return json.dumps({"art": art})

if __name__ == "__main__":
    app.run(debug=True)
