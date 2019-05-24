import flask
from flask_interface import app
from flask_socketio import SocketIO
import threading

from vrr_api.vrr_api import get_station_information
from google_calendar_api.google_calendar_api import get_calander_events_of_the_day
from weather_api.weather import get_weather_forecast

station = 'Dortmund Brackel'
number_of_upcoming_connections = 4
number_of_todays_events = 4
dortmund_id = 2935517
path_to_weather_pictograms = 'weather_pictograms/'


@app.before_first_request
def init_app():
    start_smart_mirror_updater()


def start_smart_mirror_updater():
    """ A self starting thread to update the gallery each T seconds. """
    t = threading.Timer(10.0, start_smart_mirror_updater)
    t.daemon = True
    t.start()

    connections = get_station_information(station, number_of_upcoming_connections)
    events = get_calander_events_of_the_day(number_of_todays_events)
    forecasts_dortmund = get_weather_forecast(dortmund_id, path_to_weather_pictograms)

    print(events)
    data = {'connections': connections, 'events': events,
            'forecasts': forecasts_dortmund}

    socket.emit("update", data)


# Init flask SocketIO
socket = SocketIO()
socket.init_app(app)


@app.route('/')
def smart_mirror():

    connections = get_station_information(station, number_of_upcoming_connections)


    events = get_calander_events_of_the_day(number_of_todays_events)

    #  city_name = input('Which is the city you are interested in? ')
    #  print(get_city_id(city_name))

    # relative to static folder

    forecasts_dortmund = get_weather_forecast(dortmund_id, path_to_weather_pictograms)
    return flask.render_template('smart_mirror.html', station=station,
                                  connections=connections,
                                  events=events, forecasts=forecasts_dortmund)
