import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_blinka.agnostic import sys

RST = 24
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# prepare display
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

# Prepare text
with open(os.path.expanduser("~/mission/media/messages.txt")) as f:
    lines = f.readlines()

length = len(lines)
i = 0
font = ImageFont.load_default()

while True:
    try:
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)

        if i < length:
            draw.text((0, 0), lines[i], font=font, fill=255)
            disp.image(image)
            disp.display()
            i += 1
        else:
            i = 0
        time.sleep(1)
    except:
        continue
