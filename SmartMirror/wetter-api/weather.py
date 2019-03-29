from requests import get
from datetime import datetime, timedelta
#  from json import loads, dumps
import json
from pprint import pprint

# API key for my OpenWeatherMap account
KEY = '816cb137e5f7cb33a9b6c96e757c442e'

#  cities = open('city.list.json').read()

def get_city_id(city_name):
    '''Asks for a City name
        input       city_name: string with Name of the city
        return      city_id: int with OpenWeatherMap city id'''
    city_id = False  # not yet proven that the city exists in the list
    with open('city.list.json') as f:
        citylist = json.loads(f.read())  # load city data for id numbers
    for city in citylist:
        if city['name'] == city_name:
            # the same city name could exist in different countries
            confirmation = input('Is '+city_name+' in '+city['country']+'? (y/n) ')
            if confirmation == 'y':
                city_id = city['id']
                break

    if not city_id:
        print('Sorry, this location is not available')
        exit()

    return city_id


def request_weather_data(city_id):
    '''Import the weather data of @city_id from OpenWeatherMap'''
    weather_data = get('http://api.openweathermap.org/data/2.5/forecast?id='+str(city_id)+'&APPID='+KEY).json()
    with open('forecast_{}.json'.format(city_id), 'w') as forecast:
        forecast.write(json.dumps(weather_data))
    return weather_data


def accumulate_weather_data(weather_data):
    '''Processes the imported weather data to cumulated statistic'''
    timestamps = []
    temp_max = []
    temp_min = []
    icon = []
    for forecast in weather_data['list']:
        timestamps.append(datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S'))
        temp_max.append(forecast['main']['temp_max'])
        temp_min.append(forecast['main']['temp_min'])
        icon.append(forecast['weather'][0]['icon'])
    # forecast for today saved in index 0-8
    # TODO: Hier weiter
    # forecast for tomorrow saved in index 9-16

    # TODO: Temperaturen von Kelvin in Celsius umrechnen
    return None

#  city_name = input('Which is the city you are interested in? ')
#  print(get_city_id(city_name))
dortmund_id = 2935517
#  request_weather_data(dortmund_id)
with open('forecast_{}.json'.format(dortmund_id), 'r') as forecast_data:
    weather_data = json.load(forecast_data)
#  pprint(weather_data['list'][0]['dt_txt'])
accumulate_weather_data(weather_data)
