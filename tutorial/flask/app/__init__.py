# to use the .flaskenv, install pip install python-dotenv
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/my_html')
def my_function():
    return render_template('base.html', title='Was geht')


@app.route('/my_image')
def my_image():
    image_name = 'Hackathon_SmartHome2019.png'
    return render_template('image.html', image=image_name)
