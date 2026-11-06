from unittest.mock import patch

import pytest
import requests

from weather_api import get_weather


def test_get_weather():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "current": {"temperature_2m": 15.5, "wind_speed_10m": 0.0},
            "daily": {
                "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
                "temperature_2m_max": [10.0, 11.0, 12.0],
                "temperature_2m_min": [2.0, 3.0, 4.0],
                "precipitation_sum": [0.0, 1.0, 2.0],
            },
        }
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
        mock_get.return_value.json.return_value = {
            "current": {"temperature_2m": 15.5, "wind_speed_10m": 0.0},
            "daily": {
                "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
                "temperature_2m_max": [10.0, 11.0, 12.0],
                "temperature_2m_min": [2.0, 3.0, 4.0],
                "precipitation_sum": [0.0, 1.0, 2.0],
            },
        }
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


def test_get_weather_too_few_days():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "current": {"temperature_2m": 15.5, "wind_speed_10m": 0.0},
            "daily": {
                "time": ["2026-11-06", "2026-11-07"],
                "temperature_2m_max": [10.0, 11.0],
                "temperature_2m_min": [2.0, 3.0],
                "precipitation_sum": [0.0, 1.0],
            },
        }

        with pytest.raises(ValueError, match="Not enough forecast data"):
            get_weather("Stockholm")


def test_get_weather_missing_wind_speed():
    with patch("weather_api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "current": {"temperature_2m": 15.5},
            "daily": {
                "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
                "temperature_2m_max": [10.0, 11.0, 12.0],
                "temperature_2m_min": [2.0, 3.0, 4.0],
                "precipitation_sum": [0.0, 1.0, 2.0],
            },
        }

        with pytest.raises(ValueError, match="Invalid weather data"):
            get_weather("Stockholm")
