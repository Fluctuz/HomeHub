from Screens.screen import ScreenHandler
from Apis.todoist_api import TodoistApi
from PIL import Image, ImageDraw
from datetime import datetime
import time


class TodoistScreen(ScreenHandler):

    def __init__(self, main_loop):
        super().__init__(main_loop)
        self.todoist_api = TodoistApi()
        self.font = super().get_font("pixelmix", 10)
        self.tasks = self.todoist_api.get_active_task()

    def get_bitmap_rgb(self):
        image = Image.new('P', super().dimension())
        draw = ImageDraw.Draw(image)
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            date_str = task.date.strftime("%d.%m") + ":"
            draw.text((0, i*17), date_str, 200, self.font)
            draw.text((33, i*17), task.name, 200, self.font)

        return image, (0, 50, 50)

    def update(self):
        if datetime.now().minute % 5 == 0:
            self.tasks = self.todoist_api.get_active_task()
        self.main_loop.wait(60)
