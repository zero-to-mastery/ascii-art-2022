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

IMG_FOLDER = os.path.join('static', "IMG")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * \
    1024  # File can not be largr than 16 Mb
app.config["UPLOAD_FOLDER"] = IMG_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_for_folder():
    '''Basically it will check if there are already existing folder named images or not'''
    if not Path.cwd().name == "webapp":
        print(f"{Fore.RED}Please shift to webapp directory for program to run properly. {Back.WHITE}'cd webapp'{Style.RESET_ALL}")
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
            return render_template("upload.html", file_error = "There is an error about the filename or have not passed the file. Please try again!")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img = Image.open(filepath)

            ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
            range_width = 25
            ascii_ = convert_image_to_ascii(img, range_width, ASCII_CHARS=ASCII_CHARS, fix_aspect_ratio=True)
            file.close()

            try:
                return render_template("ascii.html", ascii=ascii_)
            except Exception as e:
                return render_template("upload.html", error="Some error occurred! Try again")

    return render_template("upload.html")


@app.route("/gallery/<path:file_path>", methods=['GET', 'POST'])
def gallery(file_path=""):
    print(request.path)

    if request.form.get('char_set'):
        CHAR_SET = json.loads(request.form.get('char_set'))
    else:
        # use 1 as default if char_set is None
        CHAR_SET = ASCII_CHARS[1]

    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]

    # lagging backslash is handled differently by different browsers
    if file_path != "main" and file_path != "main/":
        file = file_path
        filename = secure_filename(file.split("/")[-1])
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        img = Image.open(filepath)
        range_width = ceil((255 + 1) / len(CHAR_SET))
        ascii_ = convert_image_to_ascii(img, range_width, ASCII_CHARS=CHAR_SET, fix_aspect_ratio=True)
        return render_template("ascii_2.html", ascii=ascii_)

    return render_template("gallery.html", imagelist=IMG_LIST)


# lagging backslash is handled differently by different browsers
@app.route("/gallery/main/", methods=["POST"])
@app.route("/gallery/main", methods=["POST"])
def remove_file():
    for file in request.form:
        os.remove(os.path.join('static', file))
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    return render_template("gallery.html", imagelist=IMG_LIST)

@app.route("/toggle_darkmode", methods=["GET"])
def toggle_darkmode():
    # If Cookie does not exist, set to False before continuing
    if request.cookies.get('darkmode') == None:
        current_state = "False"
    else:
        current_state = request.cookies.get('darkmode')

    # Toggle string values
    current_state = "True" if current_state == "False" else "False"

    response = app.make_response("There should be a cookie")
    response.set_cookie("darkmode", current_state)
    return response

if __name__ == "__main__":
    app.run(debug=True)
