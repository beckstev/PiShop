import flask
from flask_interface import app
from vrr_api.vrr_api import get_station_information
from google_calendar_api.google_calendar_api import get_calander_events_of_the_day

@app.route('/')
def smart_mirror():
    station = 'Dortmund Brackel'
    number_of_upcoming_connections = 4
    connections = get_station_information(station, number_of_upcoming_connections)

    number_of_todays_events = 4
    events = get_calander_events_of_the_day(number_of_todays_events)

    return flask.render_template('smart_mirror.html', station=station,
                                  connections=connections,
                                  events=events)
