#!/usr/bin/env python

import time
import signal

from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw

print("""hello-world.py

This basic example prints the text "Hello World" in the middle of the LCD

Press any button to see its corresponding LED toggle on/off.

Press Ctrl+C to exit.

""")

lcd.clear()

backlight.set_all(244, 66, 209)
backlight.show()

for x in range(128):
    for y in range(64):
            lcd.set_pixel(x, y, 1)

for x in range(6):
    touch.set_led(x,1)

lcd.show()

