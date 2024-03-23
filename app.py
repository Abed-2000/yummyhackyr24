from flask import Flask
from flask import render_template
from markupsafe import escape

name = "Abed"

app = Flask(__name__)

@app.route("/")
def index():
    return 'Index Page'

@app.route('/home')
@app.route('/home/<name>')
def home(name=name):
    return render_template('home.html', name=name)