from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to my weather app!"


@app.route("/weather")
def results():
    city = request.args.get("city")
    if city is None:
        return "Weather forecast"
    return city
