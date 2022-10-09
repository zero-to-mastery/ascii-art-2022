from js import document, console, Uint8Array, window, File
from pyodide import create_proxy
import asyncio
import io
from PIL import Image, ImageFilter

async def main(e):
    #Get the first file from upload
    file_list = e.target.files
    first_item = file_list.item(0)

    #Get the data from the files arrayBuffer as an array of unsigned bytes
    array_buf = Uint8Array.new(await first_item.arrayBuffer())

    #BytesIO wants a bytes-like object, so convert to bytearray first
    bytes_list = bytearray(array_buf)
    my_bytes = io.BytesIO(bytes_list) 

    try:
        CHAR_SET = int(document.getElementById("CHAR_SET").value)
        if CHAR_SET == 1:
            ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
            range_width = 25
        elif CHAR_SET ==2: 
            ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
            range_width = 32

    except:
        ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
        range_width = 32

    # ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']


    def scale_image(image, new_width=100):
        """Resizes an image preserving the aspect ratio.
        """
        (original_width, original_height) = image.size
        aspect_ratio = original_height/float(original_width)
        new_height = int(aspect_ratio * new_width)

        new_image = image.resize((new_width, new_height))
        return new_image

    def convert_to_grayscale(image):
        return image.convert('L')

    def map_pixels_to_ascii_chars(image, range_width=range_width):
        """
        Maps each pixel to an ascii char based on the range
        in which it lies.
        """

        pixels_in_image = list(image.getdata())
        pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
                pixels_in_image]

        return "".join(pixels_to_chars)

    def convert_image_to_ascii(image, new_width=100):
        image = scale_image(image)
        image = convert_to_grayscale(image)

        pixels_to_chars = map_pixels_to_ascii_chars(image)
        len_pixels_to_chars = len(pixels_to_chars)

        image_ascii = [pixels_to_chars[index: index + new_width] for index in
                range(0, len_pixels_to_chars, new_width)]

        return "\n".join(image_ascii)

    def handle_image_conversion(image_filepath):
        image = None
        try:
            image = Image.open(image_filepath)
        except Exception as e:
            print(f"Unable to open image file {image_filepath}.")
            print(e)
            return

        image_ascii = convert_image_to_ascii(image)
        return(image_ascii)

    image_file_path = my_bytes
    
    document.getElementById("ascii-output").innerHTML=""
    document.getElementById("ascii-output").innerHTML=handle_image_conversion(image_file_path)

    # Show original image
    original_image = document.createElement('img')
    original_image.src = window.URL.createObjectURL(first_item)
    document.getElementById("image").innerHTML = ""
    document.getElementById("image").appendChild(original_image)

# Run image processing code above whenever file is uploaded    
upload_file = create_proxy(main)
document.getElementById("file-upload").addEventListener("change", upload_file)