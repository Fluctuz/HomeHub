#!/usr/bin/env python
#
import signal
from gfxhat import touch, lcd, backlight, fonts


def draw(image):
    backlight.set_all(0, 100, 0)
    backlight.show()
    print("redraw")
    lcd.clear()
    for x in range(128):
        for y in range(64):
            pixel = image.getpixel((x, y))
            if pixel > 1:
               lcd.set_pixel(x, y, 1)
            else:
               lcd.set_pixel(x,y,0)
    lcd.show()


def turnOffDisplay():
    for x in range(6):
        touch.set_led(x, 0)
    backlight.set_all(0,0,0)
    backlight.show()
    lcd.clear()
    lcd.show()
