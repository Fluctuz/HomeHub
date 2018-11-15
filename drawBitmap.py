#!/usr/bin/env python
#
import signal
from gfxhat import touch, lcd, backlight, fonts


def draw(image):
    backlight.set_all(0, 100, 0)
    backlight.show()

    lcd.clear()
    for x in range(128):
        for y in range(64):
            pixel = image.getpixel((x, y))
            lcd.set_pixel(x, y, pixel)
    lcd.show()
    signal.pause()
