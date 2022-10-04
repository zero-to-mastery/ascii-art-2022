import os
import time
from flask import Flask, request, redirect, render_template
from PIL import Image
from werkzeug.utils import secure_filename
import warnings
from make_art import convert_image_to_ascii
from pathlib import Path

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
        warnings.warn(
            "\nPlease shift webapp directory for program to run functionally", DeprecationWarning)
# If this if block is not supplied then python will create the IMG_FOLDER directory outside and cause conflictions.
    if Path.cwd().name == "webapp":
        if os.path.isdir("static"):
            return print("Existing Directories Found.")
        for dirs in [IMG_FOLDER]:
            if not os.path.isdir(dirs):
                os.makedirs(dirs, mode=777)
            print("Initializig Directories...")


check_for_folder()
# Giving user time to read the message provided by the fucntion above
time.sleep(4)


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
            ascii_ = convert_image_to_ascii(img)
            file.close()

            # also delete the uploaded file from the folder
            try:
                os.remove(filepath)
                return render_template("ascii.html", ascii=ascii_)
            except Exception as e:
                return render_template("upload.html", error="Some error occurred! Try again")

    return render_template("upload.html")


@app.route("/gallery")
def gallery():
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    return render_template("gallery.html", imagelist=IMG_LIST)


if __name__ == "__main__":
    app.run(debug=True)
