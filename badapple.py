# Carlos David Sandoval Vargas.

# Import libraries.
import os
import sys
import cv2
from PIL import Image
import time

frame = -1
ASCIICharacters = [' ', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
Frames = 2191
FilePath = "./frames/frame"


# Resizes the image to fit in the terminal (with specified width).
def resizeImage(image, width=90):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int((aspect_ratio * width)/2)
    resized_image = image.resize((width, new_height)).convert('L')
    return resized_image


# Prints out the generated frame bu converting the resized image into ASCII Characters from the ASCIICharacters array.
def generateFrame(image, width=90):
    resizedImage = resizeImage(image)
    pixels = resizedImage.getdata()
    characters = "".join([ASCIICharacters[pixel//25] for pixel in pixels])
    total_pixels = len(characters)
    ASCII_image = "\n".join([characters[index:(index + width)]
                             for index in range(0, total_pixels, width)])

    sys.stdout.write(ASCII_image)


# Main loop that goes through all frames from the video.
for i in range(0, Frames):
    path = os.path.abspath(FilePath + str(i) + ".png")
    cap = Image.open(path)
    os.system('cls')
    generateFrame(cap)
    time.sleep(0.1 - (time.time() % 0.1))
