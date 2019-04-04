import flask
from flask_interface import app

from vrr_api.vrr_api import get_station_information
from google_calendar_api.google_calendar_api import get_calander_events_of_the_day
from weather_api.weather import get_weather_forecast


@app.route('/')
def smart_mirror():
    station = 'Dortmund Brackel'
    number_of_upcoming_connections = 4
    connections = get_station_information(station, number_of_upcoming_connections)

    number_of_todays_events = 4
    events = get_calander_events_of_the_day(number_of_todays_events)

    #  city_name = input('Which is the city you are interested in? ')
    #  print(get_city_id(city_name))
    dortmund_id = 2935517
    # relative to static folder
    path_to_weather_pictograms = 'weather_pictograms/'
    forecasts_dortmund = get_weather_forecast(dortmund_id, path_to_weather_pictograms)
    return flask.render_template('smart_mirror.html', station=station,
                                  connections=connections,
                                  events=events, forecasts=forecasts_dortmund)
