# Carlos David Sandoval Vargas.

# Import libraries.
from os import system, path
from sys import stdout
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from PIL import Image
from time import sleep, time
from tqdm import tqdm
from pygame import mixer

ASCIICharacters = [' ', '.', ',', ':', ';', '!', '+', '*', '?', '%', 'S', '#', '@']
asciiFrames = []

# Desired width of the each frame.
desiredWidth = 125

# Path to the frames folder.
videoFile = 'bad_apple.mp4' # mp4
audioFile = 'bad_apple.mp3' # mp3

def play_audio(audioFile):
    mixer.init()
    mixer.music.load(path.abspath(f'./{audioFile}'))
    mixer.music.play()

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

# Main loop that goes through all frames from the video.
if __name__ == '__main__':
    video = VideoCapture(path.abspath(f'./{videoFile}'))
    fps = video.get(CAP_PROP_FPS)
    totalFrames = video.get(CAP_PROP_FRAME_COUNT)
    oldWidth = video.get(CAP_PROP_FRAME_WIDTH)
    oldHeight = video.get(CAP_PROP_FRAME_HEIGHT)

    AR = oldWidth / oldHeight
    newHeight = (desiredWidth / AR) / 2
    sleepTime = 1 / fps
    
    pbar = tqdm(total=totalFrames, desc="Rendering frames", ncols=100)
    while (True):
        # Read video frame.
        ret, frame = video.read()
        
        if ret:
            generateFrame(Image.fromarray(frame), desiredWidth, newHeight)
            pbar.update(1)
        else:
            break
    pbar.close()

    play_audio(audioFile)
    for frame in asciiFrames:
        stdout.write('\033[H' + frame) # Might not woek on all terminals. Use system('cls') if this doesn't work.
        sleep(sleepTime - (time() % sleepTime)) # Make sure the time between each frame is the same.
    system('cls')