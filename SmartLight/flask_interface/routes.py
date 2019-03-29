import flask
from flask_interface import app
import numpy as np




@app.route('/')
def hello_world():
    return flask.render_template('hello_world.html')
