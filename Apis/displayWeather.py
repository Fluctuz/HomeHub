#!/usr/bin/env python

import time
import signal
from  weather_api import WeatherApi


from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw


temp = WeatherApi().current_temperature()
width, height = lcd.dimensions()
image = Image.new('P', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(fonts.AmaticSCBold, 38)
text = str(temp)
w, h = font.getsize(text)
x = (width - w) // 2
y = (height - h) // 2
draw.text((x, y), text, 1, font)

backlight.set_all(66, 243, 23)
backlight.show()
lcd.show()
