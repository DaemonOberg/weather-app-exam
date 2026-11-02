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

def test_get_weather_kiruna_coordinates():
    with patch("weather_api.requests.get") as mock_get:
        get_weather("Kiruna")
        params = mock_get.call_args.kwargs["params"]
        assert params["latitude"] == 67.86

def test_get_weather_gothenburg_coordinates():
    with patch("weather_api.requests.get") as mock_get:
        get_weather("Göteborg")
        params = mock_get.call_args.kwargs["params"]
        assert params["latitude"] == 57.71