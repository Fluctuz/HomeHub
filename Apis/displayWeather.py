#!/usr/bin/env python

import time
import signal
from  weather_api import WeatherApi


from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw

for x in range(6):
    touch.set_led(x, 1)
    time.sleep(0.1)
    touch.set_led(x, 0)

temp = WeatherApi().current_temperature()
width, height = lcd.dimensions()
image = Image.new('P', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("VCR_OSD_MONO_1.001.ttf", 21)
#font = ImageFont.truetype(fonts.AmaticSCBold, 38)
text = str(temp)
w, h = font.getsize(text)
x = (width - w) // 2
y = (height - h) // 2
draw.text((x, y), text, 1, font)

for x in range(128):
    for y in range(64):
        pixel = image.getpixel((x, y))
        lcd.set_pixel(x, y, pixel)

backlight.set_all(66, 243, 23)
backlight.show()
lcd.show()

try:
    signal.pause()
except KeyboardInterrupt:
    for x in range(6):
        backlight.set_pixel(x, 0, 0, 0)
        touch.set_led(x, 0)
    backlight.show()
    lcd.clear()
    lcd.show()

