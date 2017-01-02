
class WeatherStation:
    def __init__(self, ):
        self.sig_strength = 2


class DayForecast:
    def __init__(self):
        self.low_temp = '-'
        self.high_temp = '-'
        self.feels_like = '-'
        self.wind_speed = '-'
        self.baro = '-'
        self.wind_dir = '-'
        self.humid = '-'
        self.vis = '-'
        self.gust = '-'
        self.wind_direction = '-'
        self.rain = '-'
        self.icon = 29

    def update_day(self):
        self.low_temp = '20' + chr(0x00B0)
        self.high_temp = '27' + chr(0x00B0)
        self.feels_like = '14' + chr(0x00B0)
        self.wind_speed = '4'
        self.baro = '12'
        self.wind_dir = 'NW'
        self.humid = '2'
        self.vis = '0'
        self.gust = '5'
        self.wind_direction = 'NW'
        self.rain = '25'
        self.icon = 5


class WeatherForecasts:
    def __init__(self, days=5):
        self.forecasts = [DayForecast() for _ in range(days)]
