import httpx


MUMBAI_LATITUDE = 19.0760
MUMBAI_LONGITUDE = 72.8777


async def get_mumbai_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": MUMBAI_LATITUDE,
        "longitude": MUMBAI_LONGITUDE,
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
            url,
            params=params,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()