import forecastio
import time
from Apis.config_loader import load_config


class WeatherApi:

    def __init__(self):
        self.config = load_config()
        api_token = self.config['weather']['token']
        lat = self.config['weather']['home_lat']
        lng = self.config['weather']['home_lng']
        lang = self.config['weather']['lang']
        self.forecast = forecastio.load_forecast(api_token, lat, lng, lang=lang)

    def update(self):
        print("Weather Api update")
        api_token = self.config['weather']['token']
        lat = self.config['weather']['home_lat']
        lng = self.config['weather']['home_lng']
        lang = self.config['weather']['lang']
        forecastio.load_forecast(api_token, lat, lng, lang=lang, callback=self.on_load_finished)

    def on_load_finished(self, forecast):
        self.forecast = forecast

    def weather_code(self):
        return self.forecast.currently().icon

    def current_temperature(self):
        return str(round(self.forecast.currently().temperature, 1))


if __name__ == '__main__':
    api = WeatherApi()
    print(api.current_temperature())
    api.update()
    time.sleep(10)
    print(api.current_temperature())
