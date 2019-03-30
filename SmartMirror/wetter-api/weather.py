from requests import get
#  from datetime import datetime, timedelta, date
import datetime
#  from json import loads, dumps
import json
import os
from pprint import pprint

today = datetime.date.today()
today_str = today.strftime(format='%Y-%m-%d')
yesterday = today - datetime.timedelta(1)
yesterday_str = yesterday.strftime(format='%Y-%m-%d')

# API key for my OpenWeatherMap account
KEY = '816cb137e5f7cb33a9b6c96e757c442e'


def kelvin2celsius(t_kelvin):
    return t_kelvin - 273.15


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
    '''Import the weather forecast of @city_id from OpenWeatherMap'''
    weather_forecast = get('http://api.openweathermap.org/data/2.5/forecast?id='+str(city_id)+'&APPID='+KEY).json()
    with open('build/'+today_str+'.json', 'w') as forecast:
        forecast.write(json.dumps(weather_forecast))
    return None


def accumulate_weather_data(weather_forecast):
    '''Processes the imported weather data to cumulated statistic'''
    timestamps = []
    temp_max = []
    temp_min = []
    icons = []
    aggr_forecast = {}  # aggregated weather data
    for forecast in weather_forecast['list']:
        timestamps.append(datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S'))
        temp_max.append(forecast['main']['temp_max'])
        temp_min.append(forecast['main']['temp_min'])
        icons.append(forecast['weather'][0]['icon'])

    # weather for today saved in index 0-8, but important indices are 3-7 (9am to 6pm)
    #  aggr_forecast['today'] = timestamps[0].date().strftime(format='%a %d. %b')
    aggr_forecast['today_temp_max'] = round(kelvin2celsius(max(temp_max[3:7])), 2)
    aggr_forecast['today_temp_min'] = round(kelvin2celsius(min(temp_min[3:7])), 2)
    aggr_forecast['today_icons'] = [icon+'.png' for icon in icons[3:7]]

    # forecast for tomorrow saved in index 9-16, important are 11-15
    #  aggr_forecast['tomorrow'] = timestamps[11].date().strftime(format='%a %d. %b')
    aggr_forecast['tomorrow_temp_max'] = round(kelvin2celsius(max(temp_max[11:15])), 2)
    aggr_forecast['tomorrow_temp_min'] = round(kelvin2celsius(min(temp_min[11:15])), 2)
    aggr_forecast['tomorrow_icons'] = [icon+'.png' for icon in icons[11:15]]
    return aggr_forecast


def clean_build():
    '''Delete old forecasts from build-folder
    Delete every json file that is not a needed forecast'''
    files = os.listdir('build')
    # keep non-json files
    for index, item in enumerate(files):
        if not item.split('.')[-1] == 'json':
            files.pop(index)

    # keep relevent forecasts
    if today_str+'.json' in files:
        files.pop(files.index(today_str+'.json'))
    if yesterday_str+'.json' in files:
        files.pop(files.index(yesterday_str+'.json'))

    # delete every other json file
    for item in files:
        os.remove('build/'+item)
    return None


def main():
    # dummy functions to get the needed city id
    #  city_name = input('Which is the city you are interested in? ')
    #  print(get_city_id(city_name))
    dortmund_id = 2935517

    # create folder to save the forecasts
    if not os.path.isdir('build'):
        os.mkdir('build')

    # Start new API call if there has not been one today yet
    if not os.path.isfile('build/'+today_str+'.json'):
        request_weather_data(dortmund_id)

    # Delete older forecasts
    clean_build()

    # open forecast of yesterday (since it contains data for today)
    try:
        with open('build/'+yesterday_str+'.json', 'r') as forecast_data:
            weather_forecast = json.load(forecast_data)
    except IOError:
        with open('build/'+today_str+'.json', 'r') as forecast_data:
            weather_forecast = json.load(forecast_data)
    # WARNING: The weather data for the very first day is wrong at the moment,
    # since it is not for today and tomorrow but for the next two days

    return accumulate_weather_data(weather_forecast)


if __name__ == '__main__':
    pprint(main())
