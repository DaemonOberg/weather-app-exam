from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def weather_data():
    return {
        "current": {"temperature_2m": 15.5, "wind_speed_10m": 0.0},
        "daily": {
            "time": ["2026-11-06", "2026-11-07", "2026-11-08"],
            "temperature_2m_max": [10.0, 11.0, 12.0],
            "temperature_2m_min": [2.0, 3.0, 4.0],
            "precipitation_sum": [0.0, 1.0, 2.0],
        },
    }


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Weather Forecast" in response.data


def test_weather_route(client):
    response = client.get("/weather")
    assert response.status_code == 200


def test_weather_valid_city(client, weather_data):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.return_value = weather_data

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 200
        assert b"Stockholm" in response.data
        assert b"2026-11-06" in response.data


def test_weather_invalid_city(client):
    response = client.get("/weather?city=London")
    assert response.status_code == 400
    assert b"London" in response.data


def test_weather_uses_api(client, weather_data):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.return_value = weather_data
        client.get("/weather?city=Stockholm")
        mock_get_weather.assert_called_once_with("Stockholm")


def test_weather_api_error(client):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.side_effect = ValueError("Couldn't get weather data")

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 503
        assert b"Weather data is temporarily unavailable" in response.data


def test_404_page(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert b"404 - Page Not Found" in response.data


def test_weather_empty_city(client):
    response = client.get("/weather?city=")

    assert response.status_code == 400
    assert b"Please select a city" in response.data


def test_weather_page_contains_chart(client, weather_data):
    with patch("app.get_weather") as mock_get_weather:
        mock_get_weather.return_value = weather_data

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 200
        assert b"Max temperature" in response.data
        assert b"Min temperature" in response.data
