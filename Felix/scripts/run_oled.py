import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_blinka.agnostic import sys

import numpy as np
import sys

N_LINES_PER_SCREEN = 6
LINE_HEIGHT=11

def loadmessages():
    # Prepare text
    with open("/home/hugo/mission/media/messages.txt") as f:
        lines = f.readlines()
    lines = [x for x in lines if x.replace("\n", "").strip() != ""]
    groups = []
    for i in range(0, len(lines), N_LINES_PER_SCREEN):
        groups.append(lines[i:i+N_LINES_PER_SCREEN])
    return groups

# Prepare text
with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
    lines = f.readlines()
def get_gol_gen(matrix):
    height = 128
    width=64
    countarr = np.zeros_like(matrix)
    countarr[1:] +=    matrix[:-1]  # North
    countarr[:-1] +=   matrix[1:]  # South
    countarr[:,1:] +=  matrix[:,:-1]  # West
    countarr[:,:-1] += matrix[:,1:]  # East

    countarr[1:,1:] += matrix[:-1,:-1]  # NW
    countarr[1:,1:] += matrix[:-1,:-1]  # NE
    matrix &= (countarr == 2)
    matrix |= (countarr == 3)
    return matrix

def drawmessages(disp, data, period=.1):
    width = disp.width
    height = disp.height

    if sys.argv[1] == "gol":
        board = np.zeros((width, height), dtype=np.uint8)
        refx, refy = width//2, height//2
        init_pattern = np.array([[1, 1, 1, 0, 1], [1, 0, 0, 0, 0], [0, 0, 0, 1, 1], [0, 1, 1, 0, 1], [1, 0, 1, 0, 1]])
        for i in range(init_pattern.shape[0]):
            for j in range(init_pattern.shape[1]):
                board[refx+i, refy+j] = init_pattern[i, j]
        board[10:20, 00:60] = 1

        for step in range(1103):
            image = Image.fromarray(np.uint8((board.transpose()>0)*255), mode="L").convert("1")
            disp.image(image)
            disp.display()
            print(step)

            board = get_gol_gen(board)
            time.sleep(period)
    else:
        font = ImageFont.load_default()
        for msg in data:
            image = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image)
            for i, l in enumerate(msg):
                draw.text((0, i*LINE_HEIGHT), l, font=font, fill=255)
            disp.image(image)
            disp.display()
            print(msg)
            time.sleep(period)

def start():
    data = loadmessages()

    disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)

    # prepare display
    disp.begin()
    disp.clear()
    disp.display()
    while True:
        drawmessages(disp, data)

if __name__ == "__main__":
    start()
