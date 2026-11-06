from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Weather Forecast" in response.data


def test_weather_route(client):
    response = client.get("/weather")
    assert response.status_code == 200


def test_weather_valid_city(client):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.return_value = {
            "current": {"temperature_2m": 15.5},
            "daily": {
                "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
                "temperature_2m_max": [8.5, 9.2, 7.8],
                "temperature_2m_min": [2.1, 3.4, 1.8],
                "precipitation_sum": [0.0, 1.5, 2.3],
            },
        }

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 200
        assert b"Stockholm" in response.data
        assert b"2026-11-06" in response.data


def test_weather_invalid_city(client):
    response = client.get("/weather?city=London")
    assert response.status_code == 400
    assert b"London" in response.data


def test_weather_uses_api(client):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.return_value = {"current": {"temperature_2m": 15.5}}
        client.get("/weather?city=Stockholm")
        mock_get_weather.assert_called_once_with("Stockholm")


def test_weather_api_error(client):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.side_effect = ValueError("Couldn't get weather data")

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 503
        assert b"Weather data is temporarily unavailable" in response.data
