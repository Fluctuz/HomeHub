from abc import ABC, abstractmethod
from PIL import ImageFont
import threading


class ScreenHandler(ABC):

    def __init__(self, main_loop):
        self.main_loop = main_loop
        super().__init__()

    @staticmethod
    def get_font(name, size=15):
        return ImageFont.truetype("fonts/"+name+".ttf", size)

    @staticmethod
    def dimension():
        return 128, 64

    def btn_handler(self, channel):
        pass

    @abstractmethod
    def get_bitmap_rgb(self):
        pass

    @abstractmethod
    def update(self):
        pass
