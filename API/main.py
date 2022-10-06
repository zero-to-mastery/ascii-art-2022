import os
import re
# Import required methods from upstream folders/files
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir  = os.path.dirname(currentdir)
sys.path.append(parentdir)
from community_version import convert_image_to_ascii
# regular imports
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from werkzeug.utils import secure_filename
from rich.console import Console
from typing import Union
from PIL import Image
import requests
import shutil


# It will help to check the return values from the functions
CodingReturns = {
    "unsupported_file_format": 1,
    "cant_convert_to_ascii": 2,
    "invalid_url_string": 3,
    "url_request_error": 4,
    "cant_save_the_image": 5
}


app = FastAPI()

# function to save the uploaded image file to local directory
def save_image_file(file: UploadFile) -> str:
    # check if is the file supported or not
    if not allowed_file(file.filename):
        return CodingReturns["unsupported_file_format"]
    
    # save the file
    filename = secure_filename( file.filename )
    filepath = os.path.join( "uploads", filename )
    with open(filepath, "wb+") as f:
        f.write(file.file.read())
    return filepath

# convert the image to ASCII art and return that
def get_ascii_art(filepath) -> str:
    try:
        # read the image
        img = Image.open(filepath)
        # define the ascii characters
        ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
        # and the range width of the ascii art
        range_width = 25
        ascii_ = convert_image_to_ascii(img, range_width=range_width, ASCII_CHARS=ASCII_CHARS)
        return ascii_
    except Exception as e:
        return CodingReturns["cant_convert_to_ascii"]


# check whether is a valid image url or not
def is_valid_url(url: str) -> bool:
    # regex to check valid url
    regex = ("https?:\/\/.*\.(?:png|jpg)")
    # compile the regex
    p = re.compile(regex)

    # check the url now
    if (re.search(p, url)):
        return True
    else:
        return False

# download and save the image
def download_image_from_url(url: str) -> Union[str, int]:
    response = requests.get(url=url)

    if response.status_code == 200:
        return CodingReturns["url_request_error"]

    try:
        # get the image file name and set the file path
        filename = url.split("/")[-1]
        filepath = os.path.join("uploads", filename)
        # set the docode content to True
        response.raw.decode_content = True

        # Open a local file and save it
        with open(filepath, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        return filepath
    except Exception as e:
        return CodingReturns["cant_save_the_image"]


# only allowed extensions for the files
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# http://127.0.0.1:8000 --> home of the API
@app.get("/")
def home():
    return {"Success": "You can get the ASCII at the end point '/get-ascii' by uploading an image file as 'file' field in a JSON format. You can get raw ASCII art (or as file) at the end point '/get-ascii-file'"}


# http://127.0.0.1:8000/get-ascii --> Get the ASCII art by uploading an image file
@app.post("/get-ascii")
async def get_ascii(file: UploadFile=File(...)):
    # save the image file first
    filepath = save_image_file(file)
    if filepath == CodingReturns["unsupported_file_format"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The image file type is not matched! Only png, jpg & jpeg are allowed.")

    # convert to a ascii art
    ascii_ = get_ascii_art(filepath)
    if ascii_ == CodingReturns["cant_convert_to_ascii"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't convert the image to ascii art. Try again.")

    try:
        os.remove(filepath)
        return {"success": "Successfully created the ASCII art of the image.", "ascii_art": ascii_}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


# http://127.0.0.1:8000/get-ascii-file --> Get the ASCII art as txt format by uploading an image file
@app.post("/get-ascii-file")
def get_ascii_file(file: UploadFile=File(...)):
    # save the file first
    filepath = save_image_file(file)
    if filepath == CodingReturns["unsupported_file_format"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The image file type is not matched! Only png, jpg & jpeg are allowed.")

    # ascii art
    ascii_ = get_ascii_art(filepath)
    if ascii_ == CodingReturns["cant_convert_to_ascii"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't convert the image to ascii art. Try again.")

    try:
        # delete the image file
        os.remove(filepath)
        # now create the ascii art file
        with open("ascii_art.txt", "wt") as response_file:
            console = Console(file=response_file, record=True)
            console.print(ascii_)

        return FileResponse(os.path.join("ascii_art.txt"))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


# now, users can also get the URL by passing the Image URL
@app.get("/get-ascii-url")
def get_ascii_url(image_url: str):
    # first check, it it a valid url
    is_valid = is_valid_url(image_url)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The url is invalid. Try again using a valid image url.")

    filepath = download_image_from_url(image_url)
    if filepath == CodingReturns["cant_save_the_image"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save the image! Try again.")
    elif filepath == CodingReturns["url_request_error"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Did not get valid response from the image url. Try again")

    # ascii art
    ascii_ = get_ascii_art(filepath)
    if ascii_ == CodingReturns["cant_convert_to_ascii"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't convert the image to ascii art. Try again.")

    try:
        # delete the image file
        os.remove(filepath)
        # now create the ascii art file
        with open("ascii_art.txt", "wt") as response_file:
            console = Console(file=response_file, record=True)
            console.print(ascii_)

        return FileResponse(os.path.join("ascii_art.txt"))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

