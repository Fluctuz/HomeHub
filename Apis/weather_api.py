import forecastio
import json
import os
import asyncio


class WeatherApi:
    CONFIG_FILENAME = "config.json"

    def __init__(self):
        self.config = self.load_config()
        api_token = self.config['weather']['token']
        lat = self.config['weather']['home_lat']
        lng = self.config['weather']['home_lng']
        lang = self.config['weather']['lang']
        self.forecast = forecastio.load_forecast(api_token, lat, lng, lang=lang)

    @asyncio.coroutine
    def update(self):
        self.config = self.load_config()
        api_token = self.config['weather']['token']
        lat = self.config['weather']['home_lat']
        lng = self.config['weather']['home_lng']
        lang = self.config['weather']['lang']
        self.forecast = forecastio.load_forecast(api_token, lat, lng, lang=lang)

    def load_config(self):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__ ,self.CONFIG_FILENAME), 'r') as f:
            return json.load(f)

    def weather_code(self):
        return self.forecast.currently().icon

    def current_temperature(self):
        return str(round(self.forecast.currently().temperature, 1))


if __name__ == '__main__':
    api = WeatherApi()
    print(api.current_temperature())