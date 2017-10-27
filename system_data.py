from weather import WeatherStationWU, WeatherForecasts, IndoorSensor, WeatherStationSensor
from sensor import Sensor
import settings
import time


class SystemData:

    def __init__(self):
        sensor = Sensor(address=('192.168.0.107', 7001))
        self.ws = WeatherStationSensor(sensor)
        self.forecasts = WeatherForecasts()
        self.weather_icons = settings.wu_forecasts
        self.wind_dirs = settings.wu_wind_dirs
        self.current_date = time.strftime("%d/%m")
        self.indoor = IndoorSensor()
