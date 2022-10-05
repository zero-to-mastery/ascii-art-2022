import os
# Import required methods from upstream folders/files
import sys
from tkinter import E
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
from community_version import convert_image_to_ascii
# regular imports
from fastapi import FastAPI, UploadFile, File
from werkzeug.utils import secure_filename
from PIL import Image


app = FastAPI()

# only allowed extensions for the files
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def home():
    return {"Success": "You can get the ASCII at the end point '/get-ascii' by uploading an image file as 'file' field."}

@app.post("/get-ascii")
async def get_ascii(file: UploadFile=File(...)):
    # first check that is it our required file type
    if not allowed_file(file.filename):
        return {"error": "The file type is not matched. Only jpg, jpeg and png file is allowed!"}

    # save the file first
    filename = secure_filename( file.filename )
    filepath = os.path.join("uploads", filename)
    with open(filepath, "wb+") as f:
        f.write(file.file.read())

    # now read the image as Image obj
    img = Image.open(filepath)
    # define the ascii characters
    ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
    # and the range width of the ascii art
    range_width = 25
    # convert to a ascii art
    ascii_ = convert_image_to_ascii(img, range_width=range_width, ASCII_CHARS=ASCII_CHARS)
    # now delete the uploaded image file and send the response
    try:
        os.remove(filepath)
        return {"filename": filename, "ascii_art": ascii_}
    except Exception as e:
        return {"error": e}
