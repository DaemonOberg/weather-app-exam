from unittest.mock import patch

import pytest
import requests

from weather_api import get_weather


def test_get_weather():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"current": {"temperature_2m": 15.5}}
        result = get_weather("Stockholm")
        assert result["current"]["temperature_2m"] == 15.5


def test_get_weather_timeout():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout
        with pytest.raises(ValueError, match="Couldn't get weather data"):
            get_weather("Stockholm")


def test_get_weather_http_error():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError
        with pytest.raises(ValueError, match="Couldn't get weather data"):
            get_weather("Stockholm")


@pytest.mark.parametrize(
    "city, latitude, longitude",
    [
        ("Stockholm", 59.33, 18.07),
        ("Kiruna", 67.86, 20.23),
        ("Göteborg", 57.71, 11.97),
        ("Malmö", 55.61, 13.00),
        ("Umeå", 63.83, 20.26),
    ],
)
def test_city_coordinates(city, latitude, longitude):
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"current": {"temperature_2m": 15.5}}
        get_weather(city)
        params = mock_get.call_args.kwargs["params"]
        assert params["latitude"] == latitude
        assert params["longitude"] == longitude


def test_get_weather_empty_response():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {}

        with pytest.raises(ValueError, match="Invalid weather data"):
            get_weather("Stockholm")


def test_get_weather_incomplete_response():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"current": {}}

        with pytest.raises(ValueError, match="Invalid weather data"):
            get_weather("Stockholm")
