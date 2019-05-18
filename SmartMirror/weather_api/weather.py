from requests import get
#  from datetime import datetime, timedelta, date
import datetime
#  from json import loads, dumps
import json
import os
#  from pprint import pprint

today = datetime.date.today()
today_str = today.strftime(format='%Y-%m-%d')
yesterday = today - datetime.timedelta(1)
yesterday_str = yesterday.strftime(format='%Y-%m-%d')

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


def request_weather_data(city_id, path_to_forecast_json):
    '''Import the weather forecast of @city_id from OpenWeatherMap'''

    # To use the OpenWeather Map API we need a create a account which contain a KEY
    # This KEY is essential for the use of the API. Because the key is connected
    # with your private account you should not upload it in a public git repo
    # Therefore, the key_of_OpenWeatherMap_acc textfile is used to store the
    # KEY privatly.
    path_to_weather_api_key = os.path.dirname(__file__) + '/key_of_OpenWeatherMap_acc.txt'
    if not os.path.isfile(path_to_weather_api_key):
        raise FileNotFoundError('Cant find the file {} in your directory. Please create this file and add your personal KEY for OpenWeatherMap'.format(path_to_weather_api_key))

    else:
        KEY = 0
        with open(path_to_weather_api_key, 'r') as f:
            KEY = f.readline()[:-1]  # [:-1] to cut '\n'

    weather_forecast = get('http://api.openweathermap.org/data/2.5/forecast?id='+str(city_id)+'&APPID='+KEY).json()

    with open(os.path.join(path_to_forecast_json, today_str +'.json'), 'w') as forecast:
        forecast.write(json.dumps(weather_forecast))
    return None


def accumulate_weather_data(weather_forecast, path_to_pictograms):
    '''Processes the imported weather data to cumulated statistic'''
    timestamps = []
    temp_max = []
    temp_min = []
    icons = []
      # aggregated weather data
    for forecast in weather_forecast['list']:
        timestamps.append(datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S'))
        temp_max.append(forecast['main']['temp_max'])
        temp_min.append(forecast['main']['temp_min'])
        icons.append(os.path.join(path_to_pictograms + forecast['weather'][0]['icon']))

    # weather for today saved in index 0-8, but important indices are 3-7 (9am to 6pm)
    #  aggr_forecast['today'] = timestamps[0].date().strftime(format='%a %d. %b')
    forecast_today = {}
    forecast_today['day'] = 'Today'
    forecast_today['temp_max'] = round(kelvin2celsius(max(temp_max[3:7])), 1)
    forecast_today['temp_min'] = round(kelvin2celsius(min(temp_min[3:7])), 1)
    forecast_today['icons'] = [icon+'.png' for icon in icons[3:7]]

    # forecast for tomorrow saved in index 9-16, important are 11-15
    #  aggr_forecast['tomorrow'] = timestamps[11].date().strftime(format='%a %d. %b')
    forecast_tomorrow = {}
    forecast_tomorrow['day'] = 'Tomorrow'
    forecast_tomorrow['temp_max'] = round(kelvin2celsius(max(temp_max[11:15])), 1)
    forecast_tomorrow['temp_min'] = round(kelvin2celsius(min(temp_min[11:15])), 1)
    forecast_tomorrow['icons'] = [icon+'.png' for icon in icons[11:15]]

    aggr_forecast = [forecast_today, forecast_tomorrow]
    return aggr_forecast


def clean_build(path_to_forecast_json):
    '''Delete old forecasts from build-folder
    Delete every json file that is not a needed forecast

    Input:
    path_to_forecast_json - Path to the json files wich contain the forecast for
                            today and tomorrow
    '''
    files = os.listdir(path_to_forecast_json)
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
        os.remove(path_to_forecast_json + '/' + item)
    return None


def get_weather_forecast(city_id, path_to_pictograms):
    '''
    Input:
    city_id - OpenWeatherMap ID of your city of interest
    path_to_pictograms - path_to_weather_pictograms (.png).
                         This path is relative to the path of your
                         flask directory
    '''
    # dummy functions to get the needed city id
    #  city_name = input('Which is the city you are interested in? ')
    #  print(get_city_id(city_name))

    # The forecast returned by the api will be saved into a json file
    # This json file will be saved into the following directory
    path_to_weather_forecast_json = './flask_interface/static/build'

    # create folder to save the forecasts
    if not os.path.isdir(path_to_weather_forecast_json):
        os.mkdir(path_to_weather_forecast_json)

    # Start new API call if there has not been one today yet
    if not os.path.isfile(os.path.join(path_to_weather_forecast_json, today_str +'.json')):
        request_weather_data(city_id, path_to_weather_forecast_json)

    # Delete older forecasts
    clean_build(path_to_weather_forecast_json)

    # open forecast of yesterday (since it contains data for today)
    try:
        with open(os.path.join(path_to_weather_forecast_json, yesterday_str +'.json'), 'r') as forecast_data:
            weather_forecast = json.load(forecast_data)
    except IOError:
        with open(os.path.join(path_to_weather_forecast_json, today_str +'.json'), 'r') as forecast_data:
            weather_forecast = json.load(forecast_data)
    # WARNING: The weather data for the very first day is wrong at the moment,
    # since it is not for today and tomorrow but for the next two days

    return accumulate_weather_data(weather_forecast, path_to_pictograms)
