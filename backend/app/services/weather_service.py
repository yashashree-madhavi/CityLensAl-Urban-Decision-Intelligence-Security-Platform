import httpx


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather(
    latitude: float,
    longitude: float
):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "Asia/Kolkata"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            OPEN_METEO_URL,
            params=params,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()


async def get_weather_for_locations(locations):
    """
    Fetch current weather for multiple locations
    using a single Open-Meteo API request.
    """

    if not locations:
        return []

    latitudes = ",".join(
        str(location.latitude)
        for location in locations
    )

    longitudes = ",".join(
        str(location.longitude)
        for location in locations
    )

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "Asia/Kolkata"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            OPEN_METEO_URL,
            params=params,
            timeout=30.0
        )

        response.raise_for_status()

        return response.json()