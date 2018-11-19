from Screens.screen import ScreenHandler
from Apis.weather_api import WeatherApi
from PIL import Image, ImageDraw
from datetime import datetime
import time


class WeatherScreen(ScreenHandler):

    def __init__(self):
        super().__init__()
        self.weather_api = WeatherApi()
        self.font = super().get_font("VCR_MONO", 25)

    @staticmethod
    def _get_weather_data(weather_api):
        _weather_code = weather_api.weather_code()
        _temp = weather_api.current_temperature() + "°C"
        _time_str = datetime.now().strftime("%H:%M")
        return _weather_code, _temp, _time_str

    def get_bitmap_rgb(self):
        weather_code, temp, time_str = self._get_weather_data(self.weather_api)
        weather_icon = Image.open("Assets/weather_icons/" + weather_code + ".bmp").resize((25, 25)).convert("1")

        image = Image.new('P', super().dimension())
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), time_str, 200, self.font)
        draw.bitmap((10, 35), weather_icon, 200)
        draw.text((40, 35), temp, 200, self.font)
        return image, (0, 100, 0)

    def update(self):
        if datetime.now().minute % 5 == 0:
            self.weather_api.update()
        time.sleep(60 - datetime.now().second)
