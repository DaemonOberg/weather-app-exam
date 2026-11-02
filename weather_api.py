import requests

CITY_COORDINATES = {
    "Stockholm": (59.33, 18.07),
    "Kiruna": (67.86, 20.23),
}
def get_weather(city):
    
    latitude, longitude = CITY_COORDINATES[city]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 3,
        "timezone": "auto",
    }
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast", params=params, timeout=5
    )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise ValueError("Couldn't get weather data") from exc

