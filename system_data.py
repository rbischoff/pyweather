from weather import WeatherStation, WeatherForecasts
import settings


class SystemData:

    def __init__(self):
        self.ws = WeatherStation()
        self.forecasts = WeatherForecasts()
        self.weather_icons = settings.icons
