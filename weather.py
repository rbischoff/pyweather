import json
import requests
from settings import api_key
from sensor import Sensor
import time


def mean(numbers):
    return float(sum(numbers) / max(len(numbers), 1))


def convert_sig(rssi):
    if rssi > -50:
        return 4
    elif -51 > rssi > -65:
        return 3
    elif -66 > rssi > -80:
        return 2
    elif -81 > rssi > -95:
        return 1
    else:
        return 0


class IndoorSensor:
    def __init__(self):
        self.temp_f = '0'
        self.temp_c = '0'
        self.humidity = '0'

    def update_indoor(self):
        pass


class WeatherStationWU:
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
        self.wind_direction = 'unknown'
        self.wind_gust = '0'
        self.wind_power = 'calm'
        self.wind_avg = '0'
        self.lumen = '0'
        self.heat_index = '0'
        self.wind_chill = '0'

    def get_wind_direction(self):
        pass

    def wind_factor(self):
        if float(self.wind_speed['current']) < 11.0:
            self.wind_power = 'calm'
        elif float(self.wind_speed['current']) < 28.0:
            self.wind_power = 'mild'
        elif float(self.wind_speed['current']) < 49.0:
            self.wind_power = 'heavy'
        else:
            self.wind_power = 'severe'

    def update_station(self, daily_flush=False):
        if daily_flush:
            self._wind_speeds = []

        try:
            r = requests.post(
                'http://api.wunderground.com/api/{}/'
                'conditions/q/{}/{}.json'.format(api_key, self._state, self._city))
            self._current_json = json.loads(r.content.decode())

        except ConnectionError:
            print("Connection Failed")
            return

        try:
            self._current_json['current_observation']
        except KeyError:
            print("Update Failed")
            return

        print(self._current_json)

        try:
            self._wind_speeds.append(float(self._current_json['current_observation']['wind_mph']))
        except ValueError:
            # TODO: add a method for writing errors to a logfile.
            pass

        self.wind_avg = "{0:.1f}".format(mean(self._wind_speeds))
        self.temp['current'] = str(self._current_json['current_observation']['temp_f'])
        self.rain['current'] = str(self._current_json['current_observation']['precip_today_in'])
        self.baro['current'] = str(self._current_json['current_observation']['pressure_in'])
        self.humidity['current'] = str(self._current_json['current_observation']['relative_humidity'])
        self.wind_speed['current'] = "%d" % self._current_json['current_observation']['wind_mph']
        self.wind_direction_deg['current'] = str(self._current_json['current_observation']['wind_degrees'])
        self.wind_direction = str(self._current_json['current_observation']['wind_dir'])
        self.heat_index = str(self._current_json['current_observation']['heat_index_f'])
        self.wind_chill = str(self._current_json['current_observation']['windchill_f'])
        self.wind_gust = str(self._current_json['current_observation']['wind_gust_mph'])
        try:
            self.wind_factor()
        except ValueError:
            print("Something isn't right.")
            # Todo: write to logfile.


class WeatherStationSensor:
    def __init__(self, sensor):
        self._sensor = sensor
        self._current_json = None
        self._wind_speeds = []
        self.sig_strength = 0
        self._wind_directions = ['n', 's', 'e', 'w', 'ne', 'se', 'nw', 'sw']
        self.temp = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.rain = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.baro = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.humidity = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_speed = {'current': '0', 'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_direction_deg = {'current': '0',  'hour': '0', 'day': '0', 'week': '0', 'month': '0', 'year': '0'}
        self.wind_direction = 'unknown'
        self.wind_gust = '0'
        self.wind_power = 'calm'
        self.wind_avg = '0'
        self.lumen = '0'
        self.heat_index = '0'
        self.wind_chill = '0'

    def _update_wind_direction(self):
        wind_dirs = {'0.0': 'n', '180.0': 's', '90.0': 'e', '270.0': 'w', '45.0': 'ne', '135.0': 'se', '225.0': 'sw',
                     '315.0': 'nw', '23.0': 'ne', '68.0': 'ne', '113.0': 'se', '158.0': 'se', '203.0': 'sw',
                     '248.0': 'sw', '293.0': 'nw', '338.0': 'nw'}
        if str(self.wind_direction_deg['current']) in wind_dirs:
            self.wind_direction = wind_dirs[str(self.wind_direction_deg['current'])]

    def _update_wind_factor(self):
        if float(self.wind_speed['current']) < 11.0:
            self.wind_power = 'calm'
        elif float(self.wind_speed['current']) < 28.0:
            self.wind_power = 'mild'
        elif float(self.wind_speed['current']) < 49.0:
            self.wind_power = 'heavy'
        else:
            self.wind_power = 'severe'

    def update_station(self, verbose=False):
        self._sensor.update_history()
        data = self._sensor.get_current()
        if data:
            self.sig_strength = convert_sig(data.sig_strength)
            self.temp['current'] = str(data.temp)
            self.rain['current'] = str(data.rain)
            self.baro['current'] = str(data.baro)
            self.humidity['current'] = str(data.humidity)
            self.wind_speed['current'] = str(data.wind_speed)
            self.wind_direction_deg['current'] = str(data.wind_direction_deg)
            self.lumen = str(data.lumen)
            self._update_wind_direction()
            self._update_wind_factor()

        if verbose:
            print((self.sig_strength, self.temp['current'], self.rain['current'], self.baro['current'],
                   self.humidity['current'], self.wind_speed['current'], self.wind_direction_deg['current'],
                   self.wind_direction, self.wind_power, self.lumen))


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
    def __init__(self, days=5, state='MD', city='Odenton'):
        self._days = days
        self._state = state
        self._city = city
        self._json_forecasts = None
        self.forecasts = [DayForecast() for _ in range(days)]

    def update_forecast_data(self):
        r = requests.post(
            'http://api.wunderground.com/api/{}/'
            'forecast10day/q/{}/{}.json'.format(api_key, self._state, self._city))

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


if __name__ == '__main__':
    s = Sensor(address=('192.168.0.107', 7001))
    ws = WeatherStationSensor(sensor=s)
    while True:
        ws.update_station(verbose=True)
        time.sleep(1)
