# Carlos David Sandoval Vargas.

# Import libraries.
import os
import sys
from playsound import playsound
import cv2
from PIL import Image
import time

ASCIICharacters = [' ', '.', ',', ':', ';', '!', '+', '*', '?', '%', 'S', '#', '@']
desiredWidth = 150
asciiFrames = []

# Path to the frames folder.
videoFile = 'bad_apple.mp4' # mp4
audioFile = 'bad_apple.mp3' # mp3

# Resizes the image to fit in the terminal (with specified width).
def resizeImage(image, width, height):
    resizedImage = image.resize((int(width), int(height))).convert('L')
    return resizedImage

# Prints out the generated frame bu converting the resized image into ASCII Characters from the ASCIICharacters array.
def generateFrame(image, width, height):
    resizedImage = resizeImage(image, width, height)
    pixels = resizedImage.getdata()
    characters = "".join([ASCIICharacters[pixel//20] for pixel in pixels])
    totalPixels = len(characters)
    ASCIIimage = "\n".join([characters[index:(index + width)] for index in range(0, totalPixels, width)])
    asciiFrames.append(ASCIIimage)

def progressBar(progressDone, totalProgress):
    progressDonePercentage = progressDone / totalProgress * 100

    total = 80
    progreessString = '|'

    for i in range(0, total):
        if i <= progressDonePercentage * total / 100:
            progreessString += '█'
        else:
           progreessString += ' '
    progreessString += f'| {round(progressDonePercentage, 1)}%'

    return progreessString

# Main loop that goes through all frames from the video.
if __name__ == '__main__':
    video = cv2.VideoCapture(os.path.abspath(f'./{videoFile}'))
    fps = video.get(cv2.CAP_PROP_FPS)
    totalFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    oldWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    oldHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    AR = oldWidth / oldHeight
    newHeight = (desiredWidth / AR) / 2
    sleepTime = 1 / fps
    
    renderedFrames = 0
    while (True):
        # Read video frame.
        ret, frame = video.read()
        
        if ret:
            generateFrame(Image.fromarray(frame), desiredWidth, newHeight)
            renderedFrames += 1
            os.system('cls')
            print("Rendering frames...")
            print(progressBar(renderedFrames, totalFrames))
        else:
            break

    playsound(audioFile, False)
    for frame in asciiFrames:
        os.system('cls')
        sys.stdout.write(frame)
        time.sleep(sleepTime - (time.time() % sleepTime)) # Make sure the time between each frame is the same.
    os.system('cls')