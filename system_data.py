from weather import WeatherStation, WeatherForecasts, IndoorSensor
import settings
import time


class SystemData:

    def __init__(self):
        self.ws = WeatherStation()
        self.forecasts = WeatherForecasts()
        self.weather_icons = settings.wu_forecasts
        self.wind_dirs = settings.wu_wind_dirs
        self.current_date = time.strftime("%d/%m")
        self.indoor = IndoorSensor()
