#!/usr/bin/env python
#
from gfxhat import touch, lcd, backlight


def draw(image, rgb=(0, 100, 0)):
    backlight.set_all(rgb[0], rgb[1], rgb[2])
    backlight.show()
    lcd.clear()
    for x in range(128):
        for y in range(64):
            pixel = image.getpixel((x, y))
            if pixel > 1:
                lcd.set_pixel(x, y, 1)
            else:
                lcd.set_pixel(x,y,0)
    lcd.show()


def turn_display_off():
    for x in range(6):
        touch.set_led(x, 0)
    backlight.set_all(0,0,0)
    backlight.show()
    lcd.clear()
    lcd.show()
