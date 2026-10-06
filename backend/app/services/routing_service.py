import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOMTOM_ROUTING_URL = (
    "https://api.tomtom.com/routing/1/calculateRoute"
)


async def calculate_route(
    origin_latitude: float,
    origin_longitude: float,
    destination_latitude: float,
    destination_longitude: float
):
    api_key = os.getenv("TOMTOM_API_KEY")

    if not api_key:
        raise ValueError("TOMTOM_API_KEY is not configured")

    route_points = (
        f"{origin_latitude},{origin_longitude}:"
        f"{destination_latitude},{destination_longitude}"
    )

    params = {
        "key": api_key,
        "traffic": "true",
        "routeType": "fastest",
        "travelMode": "car",
        "maxAlternatives": 2,
    }

    url = f"{TOMTOM_ROUTING_URL}/{route_points}/json"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            timeout=20.0
        )

        response.raise_for_status()

        data = response.json()

    routes = data.get("routes", [])

    if not routes:
        raise ValueError("TomTom returned no routes")

    return data