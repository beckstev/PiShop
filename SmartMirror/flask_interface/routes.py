import flask
from flask_interface import app
from vrr_api.vrr_api import get_station_information


@app.route('/')
def smart_mirror():
    station = 'Dortmund Brackel'
    connections = get_station_information(station, 4)

    return flask.render_template('smart_mirror.html', station=station,
                                  connections=connections)
