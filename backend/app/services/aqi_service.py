import httpx


MUMBAI_LATITUDE = 19.0760
MUMBAI_LONGITUDE = 72.8777


async def get_mumbai_aqi():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": MUMBAI_LATITUDE,
        "longitude": MUMBAI_LONGITUDE,
        "current": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "european_aqi",
            "us_aqi"
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