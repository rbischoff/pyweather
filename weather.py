

class WeatherStation:
    def __init__(self):
        self.sig_strength = 2
        self._wind_directions = ['n', 's', 'e', 'w', 'ne', 'se', 'nw', 'sw']
        self.temp = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.rain = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.baro = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.humidity = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_speed = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_direction_deg = {'current': '0',  'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.lumen = '0'
        self.heat_index = '0'
        self.wind_chill = '0'

    def get_wind_direction(self):
        pass


class DayForecast:
    def __init__(self):
        self.day = '-'
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

    def update_day(self, **kwargs):
        if 'day' in kwargs:
            self.day = kwargs['day']
        if 'low_temp' in kwargs:
            self.low_temp = kwargs['low_temp'] + chr(0x00B0)
        if 'high_temp' in kwargs:
            self.high_temp = kwargs['high_temp'] + chr(0x00B0)
        if 'feels_like' in kwargs:
            self.feels_like = kwargs['feels_like'] + chr(0x00B0)
        if 'wind_speed' in kwargs:
            self.wind_speed = kwargs['wind_speed']
        if 'baro' in kwargs:
            self.baro = kwargs['bara']
        if 'wind_dir' in kwargs:
            self.wind_dir = kwargs['wind_dir']
        if 'humid' in kwargs:
            self.humid = kwargs['humid']
        if 'vis' in kwargs:
            self.vis = kwargs['vis']
        if 'gust' in kwargs:
            self.gust = kwargs['gust']
        if 'wind_direction' in kwargs:
            self.wind_direction = kwargs['wind_direction']
        if 'rain' in kwargs:
            self.rain = kwargs['rain']
        if 'icon' in kwargs:
            self.icon = kwargs['icon']


class WeatherForecasts:
    def __init__(self, days=5):
        self.forecasts = [DayForecast() for _ in range(days)]
