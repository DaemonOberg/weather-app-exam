import requests


def get_weather(city):
    params = {
        "latitude": 59.33,
        "longitude": 18.07,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 3,
        "timezone": "auto",
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast", params=params, timeout=5
    )
    response.raise_for_status()
    return response.json()
