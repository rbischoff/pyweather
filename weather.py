import json
import requests


def mean(numbers):
    return int(sum(numbers) / max(len(numbers), 1))


class WeatherStation:
    def __init__(self, state='MD', city='Fort_Meade'):
        self._state = state
        self._city = city
        self._current_json = None
        self._wind_speeds = []
        self.sig_strength = 2
        self._wind_directions = ['n', 's', 'e', 'w', 'ne', 'se', 'nw', 'sw']
        self.temp = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.rain = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.baro = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.humidity = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_speed = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_direction_deg = {'current': '0',  'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_direction = 'North'
        self.wind_gust = '0'
        self.wind_avg = '0'
        self.lumen = '0'
        self.heat_index = '0'
        self.wind_chill = '0'

    def get_wind_direction(self):
        pass

    def update_station(self, daily_flush=False):
        if daily_flush:
            self._wind_speeds = []

        r = requests.post(
            'http://api.wunderground.com/api/add326d1e4c43c31/'
            'conditions/q/{}/{}.json'.format(self._state, self._city))
        self._current_json = json.loads(r.content.decode())

        try:
            self._current_json['current_observation']
        except KeyError:
            print("Update Failed")
            return

        print(self._current_json)

        self._wind_speeds.append(int(self._current_json['current_observation']['wind_mph']))
        self.wind_avg = str(mean(self._wind_speeds))
        self.temp['current'] = str(self._current_json['current_observation']['temp_f'])
        self.rain['current'] = str(self._current_json['current_observation']['precip_today_in'])
        self.baro['current'] = str(self._current_json['current_observation']['pressure_in'])
        self.humidity['current'] = str(self._current_json['current_observation']['relative_humidity'])
        self.wind_speed['current'] = str(self._current_json['current_observation']['wind_mph'])
        self.wind_direction_deg['current'] = str(self._current_json['current_observation']['wind_degrees'])
        self.wind_direction = str(self._current_json['current_observation']['wind_dir'])
        self.heat_index = str(self._current_json['current_observation']['heat_index_f'])
        self.wind_chill = str(self._current_json['current_observation']['windchill_f'])
        self.wind_gust = str(self._current_json['current_observation']['wind_gust_mph'])


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
    def __init__(self, days=5, state='MD', city='Fort_Meade'):
        self._days = days
        self._state = state
        self._city = city
        self._json_forecasts = None
        self.forecasts = [DayForecast() for _ in range(days)]

    def update_forecast_data(self):
        r = requests.post(
            'http://api.wunderground.com/api/add326d1e4c43c31/'
            'forecast10day/q/{}/{}.json'.format(self._state, self._city))

        self._json_forecasts = json.loads(r.content.decode())
        print(self._json_forecasts)

    def update_forecasts(self):
        for i, forecast in enumerate(self.forecasts):
            forecast.update_day(
                day=self._json_forecasts['forecast']['simpleforecast']['forecastday'][i]['date']['weekday'],
                low_temp=self._json_forecasts['forecast']['simpleforecast']['forecastday'][i]['low']['fahrenheit'],
                high_temp=self._json_forecasts['forecast']['simpleforecast']['forecastday'][i]['high']['fahrenheit'],
                rain=str(self._json_forecasts['forecast']['simpleforecast']['forecastday'][i]['pop']),
                icon=self._json_forecasts['forecast']['simpleforecast']['forecastday'][i]['icon'])
