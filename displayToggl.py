#!/usr/bin/env python

from datetime import datetime
from Apis.toggl_api import TogglApi
import time
import screen_drawer

from PIL import Image, ImageFont, ImageDraw

toggl_api = TogglApi()
width, height = 128, 64
font = ImageFont.truetype("fonts/pixelmix.ttf", 15)
small_font = ImageFont.truetype("fonts/pixelmix.ttf", 8)


def create_bitmap(timer_dic, preset_projects):
    if timer_dic['id'] == "1234":
        timer_dic['start_time'] = datetime.now()
        file_name = "play.bmp"
    else:
        file_name = "pause.bmp"

    media_icon = Image.open("Assets/media_playback_icons/" + file_name).resize((25, 25)).convert("1")

    image = Image.new('P', (width, height))
    draw = ImageDraw.Draw(image)
    duration = str(abs(datetime.now() - timer_dic['start_time'])).split(".")[0]

    draw.text((2, 2), timer_dic['project_name'], 200, font)
    draw.text((2, 20), timer_dic['name'], 200, small_font)
    draw.bitmap((2, 27), media_icon, 200)
    draw.text((30, 32), duration, 200, font)
    draw.text((2, 55), preset_projects[0], 200, small_font)
    draw.text((40, 55), preset_projects[1], 200, small_font)
    draw.text((80, 55), preset_projects[2], 200, small_font)
    return image


timer_dic = toggl_api.current_timer()

try:
    counter = 0
    while True:
        preset_projects = ["Coden", "Schule", "Schlafen"]
        b_light = timer_dic['project_color']
        #create_bitmap(timer_dic, preset_projects).show()
        screen_drawer.draw(create_bitmap(timer_dic, preset_projects), b_r= b_light[0], b_g=b_light[1], b_b= b_light[2])
        if timer_dic['id'] == 1234:
            time.sleep(120)
            counter = 24
        else:
            time.sleep(0.8)
            counter += 1
        if counter % 100 == 0:
            timer_dic = toggl_api.current_timer() #update info with api

except KeyboardInterrupt:
    screen_drawer.turnOffDisplay()
