import flask
from flask_interface import app


@app.route('/')
def hello_world():
    return flask.render_template('hello_world.html')
