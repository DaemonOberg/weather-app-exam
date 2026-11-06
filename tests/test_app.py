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
        mock_get_weather.return_value = {"current": {"temperature_2m": 15.5}}

        response = client.get("/weather?city=Stockholm")

        assert response.status_code == 200
        assert b"Stockholm" in response.data


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
