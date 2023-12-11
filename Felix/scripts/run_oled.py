import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_blinka.agnostic import sys

from tqdm import tqdm
import numpy as np
import sys
import os

N_LINES_PER_SCREEN = 6
LINE_HEIGHT = 11


def loadmessages():
    # Prepare text
    with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
        lines = f.readlines()
    lines = [x for x in lines if x.replace("\n", "").strip() != ""]
    groups = []
    for i in range(0, len(lines), N_LINES_PER_SCREEN):
        groups.append(lines[i : i + N_LINES_PER_SCREEN])
    return groups


# Prepare text
with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
    lines = f.readlines()


def drawmessages(disp, data, period=0.1):
    width = disp.width
    height = disp.height

    font = ImageFont.load_default()
    for msg in data:
        image = Image.new("1", (width, height))
        draw = ImageDraw.Draw(image)
        for i, l in enumerate(msg):
            draw.text((0, i * LINE_HEIGHT), l, font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(period)


def drawvideos(disp, video_filenames, period=0.1, skip_per_n=1):
    width = disp.width
    height = disp.height

    print(f"Drawing videos, with h: {height}, w: {width}")
    np.set_printoptions(threshold=sys.maxsize)
    for vid_filename in video_filenames:
        video_data = np.load(os.path.expanduser("~/mission/media/videos/" + vid_filename))
        video_data = np.uint8(video_data)
        print(f"Showing video {vid_filename}, shape {video_data.shape}")
        if video_data.shape[1:] != (height, width):
            print(f"Video {vid_filename} has wrong shape, skipping")
            continue
        for frame_inx, img in enumerate(video_data):
            if (frame_inx % skip_per_n) != 0:
                continue
            image = Image.fromarray(img, mode="L").convert("1")
            disp.image(image)
            disp.display()

            time.sleep(period)


def start():
    data = loadmessages()
    video_filenames = [x for x in os.listdir(os.path.expanduser("~/mission/media/videos/")) if x.endswith(".npy")]

    disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)

    # prepare display
    disp.begin()
    disp.clear()
    disp.display()
    while True:
        drawmessages(disp, data)
        drawvideos(disp, video_filenames, period=(1 / 20), skip_per_n=10)


if __name__ == "__main__":
    start()
