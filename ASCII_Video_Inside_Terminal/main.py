from PIL import Image
import cv2
import time
import sys
import os
from ffpyplayer.player import MediaPlayer 
import subprocess

video_path = sys.argv[1]

def ascii_image(image):
    image = image.resize((os.get_terminal_size().columns, os.get_terminal_size().lines))
    image = image.convert('L')
    pixels = image.getdata()

    # replace each pixel with a chartacter from array
    chars = " .,-+*:;!|/\?0$W#@" #" _.,-=+:;!?0123456789$W#@N" #" _.,-=+:;cba!?0123456789$W#@N" #['@', '#', '$', '%', '^', '&', '*', ':', ';', '.', ',']
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    print("\r" + new_pixels, end="")



cap = cv2.VideoCapture(video_path)
# play audio in a seperate subprocess without any output
with open(os.devnull, 'w') as devnull:
    subprocess.Popen(['ffplay', '-nodisp', '-autoexit', video_path], stdout=devnull, stderr=devnull)
#player = MediaPlayer(video_path)
frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Frames count: ", frames_count)
fps = int(cap.get(cv2.CAP_PROP_FPS))
real_time = 1/fps


i = 0
while True:
    i += 1
    start_time = time.time()

    ret, frame = cap.read(i)
    image = Image.fromarray(frame)
    image = image.resize((os.get_terminal_size().columns, os.get_terminal_size().lines))
    image = image.convert('L')
    pixels = image.getdata()

    # replace each pixel with a chartacter from array
    chars = " .,-+*:;!|/\?0$W#@" #" _.,-=+:;!?0123456789$W#@N" #" _.,-=+:;cba!?0123456789$W#@N" #['@', '#', '$', '%', '^', '&', '*', ':', ';', '.', ',']
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    print("\r" + new_pixels, end="")


    #ascii_image(Image.fromarray(frame))
    # calculate fps
    real_fps = 1.0 / (time.time() - start_time)
    real_fps = round(real_fps, 2)
    if real_fps > fps:
        sleep_time = real_time - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
            print("\rFPS: " +  str(round( 1.0 / (time.time() - start_time), 2)), end="")
            continue

    elif real_fps < fps:
        i += 1
        ret, image = cap.read(i)
        print("\rFPS: " +  str(round( 1.0 / (time.time() - start_time), 2)), end="")
        continue
    else:
        continue