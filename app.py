from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to my weather app!"

@app.route("/weather")
def results():
    return "Weather forecast"