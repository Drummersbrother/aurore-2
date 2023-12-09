import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_blinka.agnostic import sys

import numpy as np
import sys
import os

N_LINES_PER_SCREEN = 6
LINE_HEIGHT=11

def loadmessages():
    # Prepare text
    with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
        lines = f.readlines()
    lines = [x for x in lines if x.replace("\n", "").strip() != ""]
    groups = []
    for i in range(0, len(lines), N_LINES_PER_SCREEN):
        groups.append(lines[i:i+N_LINES_PER_SCREEN])
    return groups

# Prepare text
with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
    lines = f.readlines()

def drawmessages(disp, data, period=.1):
    width = disp.width
    height = disp.height

    if sys.argv[1] == "vids":
        board = np.zeros((width, height), dtype=np.uint8)

        for img in video_data:
            image = Image.fromarray(np.uint8((img.transpose()>0)*255), mode="L").convert("1")
            disp.image(image)
            disp.display()

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
