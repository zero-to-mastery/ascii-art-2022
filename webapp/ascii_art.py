import os
import time
from flask import Flask, flash, request, redirect, render_template, url_for
from PIL import Image
from werkzeug.utils import secure_filename
import warnings
from make_art import convert_image_to_ascii

IMG_FOLDER = os.path.join('static', "IMG")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * \
    1024  # File can not be largr than 16 Mb
app.config["UPLOAD_FOLDER"] = IMG_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_for_folder():
    '''Basically it will check if there are already existing folder named images and gallery or not'''
    if not os.getcwd() == "webapp":
        warnings.warn(
            "\nPlease shift webapp directory for program to run functionally", DeprecationWarning)
# If this if block is not supplied then python will create the IMG_FOLDER directory outside and cause conflictions.
        return
    for dirs in [IMG_FOLDER]:
        if not os.path.isdir(dirs):
            os.makedirs(dirs, mode=777)
        print("Initializig Directories...")


check_for_folder()
# Giving user time to read the messages provided by the fucntion above
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
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img = Image.open(filepath)
            ascii_ = convert_image_to_ascii(img)
            # file.save("./gallery") Giving Permission denied error so just used image folder instead. Solve it if you can please
            file.close()
            return render_template("ascii.html", ascii=ascii_)
    return render_template("upload.html")


@app.route("/gallery")
def gallery():
    IMG_LIST = os.listdir('static/IMG')
    IMG_LIST = ['IMG/' + i for i in IMG_LIST]
    return render_template("gallery.html", imagelist=IMG_LIST)


if __name__ == "__main__":
    app.run(debug=True)