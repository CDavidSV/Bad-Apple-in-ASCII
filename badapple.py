# Carlos David Sandoval Vargas.

# Import libraries.
import os
import sys
from playsound import playsound
import cv2
from PIL import Image
import time

ASCIICharacters = [' ', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
desiredWidth = 150

# Path to the frames folder.
fileName = 'bad_apple1.mp4'

# Resizes the image to fit in the terminal (with specified width).
def resizeImage(image, width, height):
    resizedImage = image.resize((int(width), int(height))).convert('L')
    return resizedImage

# Prints out the generated frame bu converting the resized image into ASCII Characters from the ASCIICharacters array.
def generateFrame(image, width, height):
    resizedImage = resizeImage(image, width, height)
    pixels = resizedImage.getdata()
    characters = "".join([ASCIICharacters[pixel//25] for pixel in pixels])
    totalPixels = len(characters)
    ASCIIimage = "\n".join([characters[index:(index + width)] for index in range(0, totalPixels, width)])
    sys.stdout.write(ASCIIimage)


# Main loop that goes through all frames from the video.
if __name__ == '__main__':
    video = cv2.VideoCapture(os.path.abspath(f'./{fileName}'))
    fps = video.get(cv2.CAP_PROP_FPS)
    oldWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    oldHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    AR = oldWidth / oldHeight
    newHeight = (desiredWidth / AR) / 2
    sleepTime = 1 / fps

    playsound("bad_apple.mp3", False)
    while (True):
        # Read video frame.
        ret, frame = video.read()

        if ret:
            os.system('cls')
            generateFrame(Image.fromarray(frame), desiredWidth, newHeight)
            time.sleep(sleepTime - (time.time() % sleepTime))
        else:
            break