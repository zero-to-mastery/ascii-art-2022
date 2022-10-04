import os
import time
from flask import Flask, flash, request, redirect, render_template, url_for
from PIL import Image
from werkzeug.utils import secure_filename
from make_art import convert_image_to_ascii
from pathlib import Path
from colorama import Fore, Back, Style
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
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img = Image.open(filepath)
            ascii_ = convert_image_to_ascii(img)
            file.close()
            return render_template("ascii.html", ascii=ascii_)
    return render_template("upload.html")


@app.route("/gallery/<path:file_path>")
def gallery(file_path=""):
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    if file_path != "main":
        file = file_path
        filename = secure_filename(file.split("/")[1])
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        img = Image.open(filepath)
        ascii_ = convert_image_to_ascii(img)
        return render_template("ascii.html", ascii=ascii_)

    return render_template("gallery.html", imagelist=IMG_LIST)


if __name__ == "__main__":
    app.run(debug=True)
