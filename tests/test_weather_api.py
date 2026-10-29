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
        with pytest.raises(requests.exceptions.Timeout):
            get_weather("Stockholm")
