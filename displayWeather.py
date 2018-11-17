#!/usr/bin/env python

from datetime import datetime
from Apis.weather_api import WeatherApi
import time
import screen_drawer

from PIL import Image, ImageFont, ImageDraw

weather_api = WeatherApi()
width, height = 128, 64 #lcd.dimensions()
font = ImageFont.truetype("fonts/VCR_MONO.ttf", 25)


def get_data(api):
    _weather_code = api.weather_code()
    _temp = api.current_temperature() + "°C"
    _time_str = datetime.now().strftime("%H:%M")
    return _weather_code, _temp, _time_str


def create_bitmap(weather_code, temp, time_str):
    weather_icon = Image.open("Assets/weather_icons/"+weather_code+".bmp").resize((25, 25)).convert("1")
    image = Image.new('P', (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), time_str, 200, font)
    draw.bitmap((10, 35), weather_icon, 200)
    draw.text((40, 35), temp, 200, font)
    return image


def draw_bitmap():
    weather_code, temp, time_str = get_data(weather_api)
    #create_bitmap(weather_code, temp, time_str).show()
    screen_drawer.draw(create_bitmap(weather_code, temp, time_str))


draw_bitmap()
time.sleep(60 - datetime.now().second)


try:
    while True:
        draw_bitmap()
        if datetime.now().minute % 5 == 0:
            weather_api.update()
        time.sleep(60)
except KeyboardInterrupt:
    screen_drawer.turnOffDisplay()
