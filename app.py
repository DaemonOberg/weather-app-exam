from flask import Flask, render_template, request

from cities import is_valid_city
from weather_api import get_weather

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather")
def results():
    city = request.args.get("city")

    if city is None:
        return "Weather forecast"

    if not is_valid_city(city):
        return f"Invalid city: {city}", 400

    try:
        weather = get_weather(city)
        return render_template("weather.html", city=city, weather=weather)
    except ValueError:
        return "Weather data is temporarily unavailable", 503
