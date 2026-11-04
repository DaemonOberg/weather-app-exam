from flask import Flask, request

from cities import is_valid_city

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to my weather app!"


@app.route("/weather")
def results():
    city = request.args.get("city")
    if city is None:
        return "Weather forecast"
    if not is_valid_city(city):
        return f"Invalid city: {city}", 400
    return city
