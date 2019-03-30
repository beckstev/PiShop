# coding: utf-8
from flask import Flask

# Start Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "PeP_et_al_PiShop"

from flask_interface import routes
