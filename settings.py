import api
sd = 'forecast/'  # Icon sub-directory name.

# The forcast includes an icon index number.  Below is an ordered array that has the
# icon filename for the icon index.

ICON_TYPES = ['.png']
ICON_BASE_DIR = '/icons/'
COMPASS_DIR = ICON_BASE_DIR + 'compass/'
ICON_DICTIONARY = {'weather_station': 'weather_station/weather_station.png',
                   'sig0': 'weather_station/cell_sig0.png',
                   'sig1': 'weather_station/cell_sig1.png',
                   'sig2': 'weather_station/cell_sig2.png',
                   'sig3': 'weather_station/cell_sig3.png',
                   'sig4': 'weather_station/cell_sig4.png'
                   }

icons = [
    sd + 'thunderstorm.png',         # 0 - Thunderstorms
    sd + 'windy.png',                # 1 - Windy Rain
    sd + 'unknown.png',              # 2 - Windy Rain
    sd + 'thunderstorm.png',         # 3 - Thunderstorms
    sd + 't-storms2.png',            # 4 - T-Storms
    sd + 'rain_snow.png',            # 5 - Rain Snow
    sd + 'rain_snow.png',            # 6 - Rain Sleet
    sd + 'rain_snow.png',            # 7 - Snow/Rain Icy Mix
    sd + 'rain_snow.png',            # 8 - Freezing Drizzle
    sd + 'rain.png',                 # 9 - Drizzle
    sd + 'rain.png',                 # 10 - Freezing Rain
    sd + 't-showers.png',            # 11 - T-Showers
    sd + 'rain.png',                 # 12 - Heavy Rain
    sd + 'snow.png',                 # 13 - Snow Flurries
    sd + 'snow.png',                 # 14 - Light Snow
    sd + 'snow.png',                 # 15 - Snowflakes
    sd + 'snow.png',                 # 16 - Heavy Snow
    sd + 'thunderstorm.png',         # 17 - Thunderstorms
    sd + 'unknown.png',              # 18 - Hail
    sd + 'unknown.png',              # 19 - Dust
    sd + 'fog.png',                  # 20 - Fog
    sd + 'fog.png',                  # 21 - Haze
    sd + 'fog.png',                  # 22 - Smoke
    sd + 'windy.png',                # 23 - Windy
    sd + 'windy.png',                # 24 - Windy
    sd + 'sunny.png',                # 25 - Frigid
    sd + 'partly_cloudy.png',        # 26 - Cloudy
    sd + 'partly_cloudy.png',        # 27 - Mostly Cloudy Night (the "Night" will not be included)
    sd + 'mostly_cloudy.png',        # 28 - Mostly Cloudy
    sd + 'partly_cloudy.png',        # 29 - Partly Cloudy Night (the "Night" will not be included)
    sd + 'partly_cloudy.png',        # 30 - Partly Cloudy
    sd + 'clear_night.png',          # 31 - Clear Night (the "Night" will not be included)
    sd + 'sunny.png',                # 32 - Sunny
    sd + 'sunny.png',                # 33 - Fair
    sd + 'sunny.png',                # 34 - Fair
    sd + 'thunderstorm.png',         # 35 - Thunderstorms
    sd + 'sunny.png',                # 36 - Hot
    sd + 'scattered_tstorms.png',    # 37 - Isolated Thunder
    sd + 'scattered_tstorms.png',    # 38 - Scattered T-Storms
    sd + 'calm_rain1.png',           # 39 - Scattered Rain
    sd + 'rain.png',                 # 40 - Heavy Rain
    sd + 'snow.png',                 # 41 - Scattered Snow
    sd + 'snow.png',                 # 42 - Heavy Snow
    sd + 'snow.png',                 # 43 - Windy/Snowy
    sd + 'mostly_cloudy.png',        # 44 - Partly Cloudy Day
    sd + 'rain.png',                 # 45 - Scattered Showers Night (the "Night" will not be included)
    sd + 'snow.png',                 # 46 - Snowy Night
    sd + 'scattered_tstorms.png'     # 47 - Scattered T-Storms Night (the "Night" will not be included)
]

wu_forecasts = {
    'chanceofflurries': sd + 'chanceflurries.png',
    'chanceofrain': sd + 'chancerain.png',
    'chancerain': sd + 'chancerain.png',
    'chancefreezingrain': sd + 'chancesleet.png',
    'chanceofsleet': sd + 'chancesleet.png',
    'chanceofsnow': sd + 'chancesnow.png',
    'chanceofthunderstorms': sd + 'chancetstorms.png',
    'chanceofathunderstorm':	sd + 'chancetstorms.png',
    'clear': sd + 'clear.png',
    'cloudy': sd + 'cloudy.png',
    'flurries': sd + 'flurries.png',
    'fog': sd + 'fog.png',
    'haze': sd + 'hazy.png',
    'mostlycloudy': sd + 'mostlycloudy.png',
    'mostlysunny': sd + 'mostlysunny.png',
    'partlycloudy': sd + 'partlycloudy.png',
    'partlysunny': sd + 'partlysunny.png',
    'freezingrain': sd + 'sleet.png',
    'rain': sd + 'rain.png',
    'sleet': sd + 'sleet.png',
    'snow': sd + 'snow.png',
    'sunny': sd + 'sunny.png',
    'thunderstorms': sd + 'thunderstorm.png',
    'thunderstorm': sd + 'thunderstorm.png',
    'unknown': sd + 'unknown.png',
    'overcast':	 sd + 'cloudy.png',
    'scatteredclouds': sd + 'partlycloudy.png'
}

wu_wind_dirs = {
    'East': 'e',
    'ENE': 'ne',
    'ESE': 'se',
    'NE': 'ne',
    'NNE': 'ne',
    'NNW':	'nw',
    'North': 'n',
    'NW': 'nw',
    'SE': 'se',
    'South': 's',
    'SSE': 's',
    'SSW':	'sw',
    'SW': 'sw',
    'Variable' : 'n',
    'West': 'w',
    'WNW': 'nw',
    'WSW': 'sw'
}

# Feel free to just add your api key here, just don't push it to remote repos like I did.  I had to change my key.
api_key = api.key