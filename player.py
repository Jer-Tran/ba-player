import sys
import subprocess
import pyautogui as gui
import time
from PIL import Image
import numpy as np
import os
import cv2

gui.PAUSE=0     # Maximising fps

cols = 80
scale = 0.43
gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def valid_video(filename):
    return True

def getAverageL(image):
 
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
 
    # get shape
    w,h = im.shape
 
    # get average
    return np.average(im.reshape(w*h))

# Essentially from here
# https://www.geeksforgeeks.org/converting-image-ascii-image-python/
def file_to_ascii(filename, cols, scale):
    gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # Convert image to PIL form
    image = Image.open(filename).convert('L')

    # Getting width/height of original image, and scaling
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale
    rows = int(H/h)

    # Error checking for scalabiltiy
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    out = []

    # For each output row
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # Sets upper bound for 
        if j == rows-1:
            y2 = H
        
        # Empty string for the row, which gets added to in next loop
        out.append("")

        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # Sets upper bound for
            if i == cols-1:
                x2 = W

            # Gets relevant pixel(s) to convert to greyscale
            img = image.crop((x1, y1, x2, y2))

            # Average Luminence
            avg = int(getAverageL(img))
            out[j] += gscale[int((avg*69)/255)]
            
    return out

# Converts from 
def img_to_ascii(img, cols, scale):
    gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    # Convert image to PIL form
    image = img.convert('L')

    # Getting width/height of original image, and scaling
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale
    rows = int(H/h)

    # Error checking for scalabiltiy
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    out = []

    # For each output row
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # Sets upper bound for 
        if j == rows-1:
            y2 = H
        
        # Empty string for the row, which gets added to in next loop
        out.append("")

        for i in range(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # Sets upper bound for
            if i == cols-1:
                x2 = W

            # Gets relevant pixel(s) to convert to greyscale
            img = image.crop((x1, y1, x2, y2))

            # Average Luminence
            avg = int(getAverageL(img))
            out[j] += gscale[int((avg*69)/255)]
            
    return out

# Scraps of attempting to modify a currently open notepad application
# https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

# Printing the contents of a file into terminal
def terminal_player(filename):    

    # Capture the video in form of multiple captures
    cap = cv2.VideoCapture(filename)

    image_counter = 0
    read_counter = 0
    frame_step = 1

    # For each frame in the video
    while(cap.isOpened()):
        ret, cv2_im = cap.read()
        if ret and read_counter % frame_step == 0:
            converted = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
    
            pil_im = Image.fromarray(converted)
            img = img_to_ascii(pil_im, cols, scale)

            out = ""
            # Print every frame to output
            for row in img:
                out += f"\n{row}|"
            
            os.system('cls||clear') # Greatly reduces frame tearing, but still jittery and reduce frame rate a lot
            # Just for framing the output to make it look prettier
            for col in range(len(img[0]) + 1):
                if col == len(img[0]):
                    print('+', end='')
                else:
                    print('-', end='')
            print(out)
        
        elif not ret:
            break
        
        read_counter += 1

    # Releases capture once all frames are processed
    cap.release()

# Gets contents of a video file, and plays it in ascii form inside of an open Notepad window, using user keyboard inputs
# If possible, do it in dynamic scaling
# Inspired by https://www.youtube.com/watch?v=itbBubDqm70
#   In the video, they played Bad Apple in MSPaint by using mouse inputs
def notepad_player(filename):
    # Check if filename is valid

    # Check if a Notepad window is open
        # Unsure how to actually accomplish this, for now just opens a new notepad
        # Using windows 11 to open notepad, may not work on other OS or versions
    # if not process_exists("Notepad.exe"):
    #     print("Error: Please check there is an open Notepad window")
    #     sys.exit(1)
    gui.press('win')
    time.sleep(0.5)
    gui.write('notepad', interval=0.1)
    time.sleep(0.5)
    gui.press('enter')
    time.sleep(3)

    # # Open file, for each frame
    # FRAME = 5258

    # for frame in range(5258):
    #     # img = convertImageToAscii(f"./frames/frame{frame + 1}.png", cols, scale, True)
    #     img = file_to_ascii(f"./frames/frame{frame + 1}.png", cols, scale)

    #     out = ""
    #     # Print every frame to output
    #     for row in img:
    #         out += f"\n{row}"
        
    #     gui.write(out, interval=0.0001)
    #     time.sleep(1)
    #     for row in img:
    #         for col in range(len(img[0]) + 1):
    #             gui.press('backspace')

    cap = cv2.VideoCapture(filename)

    image_counter = 0
    read_counter = 0
    frame_step = 1

    # For each frame in the video
    while(cap.isOpened()):
        ret, cv2_im = cap.read()
        if ret and read_counter % frame_step == 0:
            converted = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
    
            pil_im = Image.fromarray(converted)
            img = img_to_ascii(pil_im, cols, scale)

            out = ""
            # Print every frame to output
            for row in img:
                out += f"\n{row}"
            
            gui.write(out, interval=0.0001)
            time.sleep(1)
            for row in img:
                for col in range(len(img[0]) + 1):
                    gui.press('backspace')
        
        elif not ret:
            break
        
        read_counter += 1

    # Releases capture once all frames are processed
    cap.release()

def main():
    # print(sys.argv)
    if len(sys.argv) < 3:
        print(f"Usage: ./{sys.argv[0]} (player option) (video filename)")
        sys.exit(1)

    opt = sys.argv[1]
    filename = sys.argv[2]

    # Check it is a valid video file
    if not valid_video(filename):           # Currently irrelevant, always will pull from png file
        sys.exit(1)

    if opt == '1':        # Might change to constant names later
        terminal_player(filename)
    elif opt == '2':
        notepad_player(filename)
    else:
        print("Invalid player option")
        print("Valid player options are:")
        options = '''1. Play video in terminal
2. Play video in notepad'''
        print(options)
    print("Done")

if __name__ == "__main__":
    main()