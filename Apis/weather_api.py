import forecastio
import json


class WeatherApi:
    CONFIG_FILENAME = "config.json"

    def __init__(self):
        self.config = self.load_config()
        api_token = self.config['weather']['token']
        lat = self.config['weather']['home_lat']
        lng = self.config['weather']['home_lng']
        lang = self.config['weather']['lang']
        self.forecast = forecastio.load_forecast(api_token, lat, lng, lang=lang)

    def load_config(self):
        with open(self.CONFIG_FILENAME, 'r') as f:
            return json.load(f)

    def current_temperature(self):
        return self.forecast.currently().temperature


if __name__ == '__main__':
    api = WeatherApi()
    print(api.current_temperature())