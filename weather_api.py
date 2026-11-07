import requests

CITY_COORDINATES = {
    "Stockholm": (59.33, 18.07),
    "Kiruna": (67.86, 20.23),
    "Göteborg": (57.71, 11.97),
    "Malmö": (55.61, 13.00),
    "Umeå": (63.83, 20.26),
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
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Invalid weather data")  # noqa: TRY004

        current = data.get("current")
        daily = data.get("daily")

        if not isinstance(current, dict):
            raise ValueError("Invalid weather data")  # noqa: TRY004

        if not isinstance(daily, dict):
            raise ValueError("Invalid weather data")  # noqa: TRY004

        if current.get("temperature_2m") is None:
            raise ValueError("Invalid weather data")

        if current.get("wind_speed_10m") is None:
            raise ValueError("Invalid weather data")

        required_daily_fields = (
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
        )

        for field in required_daily_fields:
            values = daily.get(field)

            if not values:
                raise ValueError("Invalid weather data")

            if len(values) < 3:
                raise ValueError("Not enough forecast data")
            
            if any(value is None for value in values[:3]):
                raise ValueError("Invalid weather data")

        if len(daily.get("time", [])) < 3:
            raise ValueError("Not enough forecast data")

        return data

    except requests.RequestException as exc:
        raise ValueError("Couldn't get weather data") from exc
