import os
import httpx
import math

from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_URL = (
    "https://api.tomtom.com/traffic/services/4/"
    "flowSegmentData/absolute/10/json"
)


def calculate_congestion(
    current_speed: float,
    free_flow_speed: float
):
    if not free_flow_speed or free_flow_speed <= 0:
        return {
            "congestion_percentage": 0,
            "congestion_level": "UNKNOWN"
        }

    congestion_percentage = (
        (free_flow_speed - current_speed)
        / free_flow_speed
    ) * 100

    congestion_percentage = max(
        0,
        min(congestion_percentage, 100)
    )

    if congestion_percentage >= 70:
        congestion_level = "SEVERE"
    elif congestion_percentage >= 50:
        congestion_level = "HIGH"
    elif congestion_percentage >= 25:
        congestion_level = "MODERATE"
    else:
        congestion_level = "LOW"

    return {
        "congestion_percentage": round(
            congestion_percentage, 2
        ),
        "congestion_level": congestion_level
    }

def calculate_nearest_road_distance(
    latitude: float,
    longitude: float,
    coordinates: dict
):
    points = coordinates.get("coordinate", [])

    if not points:
        return None

    def haversine_distance(
        lat1,
        lon1,
        lat2,
        lon2
    ):
        R = 6371000

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        return 2 * R * math.asin(
            math.sqrt(a)
        )

    distances = [
        haversine_distance(
            latitude,
            longitude,
            point["latitude"],
            point["longitude"]
        )
        for point in points
    ]

    return round(min(distances), 2)

async def get_traffic(
    latitude: float,
    longitude: float
):
    api_key = os.getenv("TOMTOM_API_KEY")

    if not api_key:
        raise ValueError(
            "TOMTOM_API_KEY is not configured"
        )

    params = {
        "point": f"{latitude},{longitude}",
        "key": api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            TOMTOM_API_URL,
            params=params,
            timeout=15.0
        )

        response.raise_for_status()

        data = response.json()

    flow = data.get("flowSegmentData")

    if not flow:
        raise ValueError(
            "TomTom returned no traffic flow data"
        )

    current_speed = flow.get("currentSpeed")
    free_flow_speed = flow.get("freeFlowSpeed")

    congestion = calculate_congestion(
        current_speed,
        free_flow_speed
    )
    road_distance = calculate_nearest_road_distance(
        latitude,
        longitude,
        flow.get("coordinates", {})
    )

    return {
        "current_speed": current_speed,
        "free_flow_speed": free_flow_speed,
        "current_travel_time": flow.get(
            "currentTravelTime"
        ),
        "free_flow_travel_time": flow.get(
            "freeFlowTravelTime"
        ),
        "confidence": flow.get("confidence"),
        "road_closure": flow.get("roadClosure"),

        "congestion_percentage":
            congestion["congestion_percentage"],

        "congestion_level":
            congestion["congestion_level"],

        "distance_to_road_meters": 
            road_distance,

        "coordinates": flow.get("coordinates")
    }