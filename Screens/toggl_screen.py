from Screens.screen import ScreenHandler
from Apis.toggl_api import TogglApi
from PIL import Image, ImageDraw
import time
from datetime import datetime


class TogglScreen(ScreenHandler):

    def __init__(self):
        super().__init__()
        self.toggl_api = TogglApi()
        self.previous_minute_update = -1
        self.timer_dic = self.toggl_api.current_timer()
        self.preset_projects = self.toggl_api.preset_projects()[0]
        self.font = super().get_font("pixelmix", 10)
        self.small_font = super().get_font("pixelmix", 8)

    def btn_handler(self, channel):
        if channel == 2:
            return False
        elif channel == 0:
            pre = self.toggl_api.preset_projects()
            self.preset_projects = pre[(pre.index(self.preset_projects)+1)%len(pre)]
        elif channel == 1:
            self.toggl_api.stop_timer()
            self.timer_dic = self.toggl_api.current_timer()
        elif channel >= 3: # 3 - 5
            self.toggl_api.start_timer(self.preset_projects[channel - 3], "")
            self.timer_dic = self.toggl_api.current_timer()  # update info with api
        return True

    def get_bitmap_rgb(self):
        if self.timer_dic['id'] == "1234":  # Not running
            file_name = "play.bmp"
            duration = "00:00:00"
        else:
            file_name = "pause.bmp"
            duration = str(abs(datetime.now() - self.timer_dic['start_time'])).split(".")[0]

        media_icon = Image.open("Assets/media_playback_icons/" + file_name).resize((25, 25)).convert("1")
        image = Image.new('P', super().dimension())
        draw = ImageDraw.Draw(image)

        draw.text((2, 2),  self.timer_dic['project_name'], 200, self.font)
        draw.text((2, 20),  self.timer_dic['name'], 200, self.small_font)
        draw.bitmap((2, 27), media_icon, 200)
        draw.text((30, 32), duration, 200, self.font)
        draw.text((2, 55), self.preset_projects[0], 200, self.small_font)
        draw.text((40, 55), self.preset_projects[1], 200, self.small_font)
        draw.text((80, 55), self.preset_projects[2], 200, self.small_font)
        return image,  self.timer_dic['project_color']

    # DON'T refactor current_minute
    def update(self):
        if self.timer_dic['id'] == "1234":
            for i in range(36):
                if self.timer_dic['id'] != "1234": #other thread and stuff
                   break
                time.sleep(5)
            self.timer_dic = self.toggl_api.current_timer()  # update info with api
        else:
            time.sleep(2)  # Sleep some time than update clock
            current_minute = datetime.now().minute
            # Update Info every 3 min and prevent update multiple time per minute
            if current_minute % 3 == 0 and current_minute != self.previous_minute_update:
                self.previous_minute_update = current_minute
                self.timer_dic = self.toggl_api.current_timer()  # update info with api
