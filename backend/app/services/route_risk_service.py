import math
from app.models.emergency import Emergency

def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
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

    return 2 * R * math.asin(math.sqrt(a))


def is_route_near_location(
    route_point,
    location_latitude,
    location_longitude,
    radius_meters=500
):
    distance = haversine_distance(
        route_point["latitude"],
        route_point["longitude"],
        location_latitude,
        location_longitude
    )

    return distance <= radius_meters

from sqlalchemy.orm import Session

from app.models.bmc_weather import BMCWeatherData
from app.services.flood_risk_service import calculate_flood_risk


def get_nearby_flood_risks(
    db: Session,
    route_points,
    radius_meters=150
):
    nearby_risks = []

    stations = (
        db.query(BMCWeatherData)
        .all()
    )

    for station in stations:
        for route_point in route_points:

            if is_route_near_location(
                route_point,
                station.latitude,
                station.longitude,
                radius_meters
            ):
                try:
                    risk = calculate_flood_risk(
                        db,
                        station.bmc_location_id
                    )
                    if risk is None:
                        continue

                    if risk["data_status"] == "UNAVAILABLE":
                        continue
                    nearby_risks.append({
                        "station_id": station.id,
                        "station_name": station.station_name,
                        "latitude": station.latitude,
                        "longitude": station.longitude,
                        "flood_risk": risk
                    })

                except Exception:
                    continue

                
                break

    return nearby_risks

def get_nearby_emergencies(
    db: Session,
    route_points,
    radius_meters=300
):
    nearby_emergencies = []

    if not route_points:
        return nearby_emergencies

    origin_point = route_points[0]
    destination_point = route_points[-1]

    emergencies = (
        db.query(Emergency)
        .filter(
            Emergency.status.in_(
                ["active", "dispatched"]
            )
        )
        .all()
    )

    for emergency in emergencies:

        closest_distance = None
        closest_route_point = None

        for route_point in route_points:

            distance = haversine_distance(
                route_point["latitude"],
                route_point["longitude"],
                emergency.latitude,
                emergency.longitude
            )

            if (
                closest_distance is None
                or distance < closest_distance
            ):
                closest_distance = distance
                closest_route_point = route_point

        if (
            closest_distance is None
            or closest_distance > radius_meters
        ):
            continue

        # Check whether the emergency is near the origin
        origin_distance = haversine_distance(
            origin_point["latitude"],
            origin_point["longitude"],
            emergency.latitude,
            emergency.longitude
        )

        # Check whether the emergency is near the destination
        destination_distance = haversine_distance(
            destination_point["latitude"],
            destination_point["longitude"],
            emergency.latitude,
            emergency.longitude
        )

        if origin_distance <= radius_meters:
            location_type = "ORIGIN"

        elif destination_distance <= radius_meters:
            location_type = "DESTINATION"

        else:
            location_type = "ALONG_ROUTE"

        nearby_emergencies.append({
            "emergency_id": emergency.id,
            "emergency_type": emergency.emergency_type,
            "description": emergency.description,
            "latitude": emergency.latitude,
            "longitude": emergency.longitude,
            "status": emergency.status,
            "distance_meters": round(
                closest_distance,
                2
            ),
            "location_type": location_type
        })

    return nearby_emergencies

def get_nearby_incidents(
    db: Session,
    route_points,
    radius_meters=300
):
    nearby_incidents = []

    if not route_points:
        return nearby_incidents

    from app.models.incident_report import IncidentReport

    incidents = (
        db.query(IncidentReport)
        .filter(
            IncidentReport.status.in_(
                ["verified", "investigating"]
            )
        )
        .all()
    )

    for incident in incidents:
        closest_distance = None

        for route_point in route_points:
            distance = haversine_distance(
                route_point["latitude"],
                route_point["longitude"],
                incident.latitude,
                incident.longitude
            )

            if (
                closest_distance is None
                or distance < closest_distance
            ):
                closest_distance = distance

        if (
            closest_distance is None
            or closest_distance > radius_meters
        ):
            continue

        nearby_incidents.append({
            "incident_id": incident.id,
            "incident_type": incident.incident_type,
            "description": incident.description,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "status": incident.status,
            "distance_meters": round(
                closest_distance,
                2
            )
        })

    return nearby_incidents