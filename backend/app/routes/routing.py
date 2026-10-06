from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.services.routing_service import calculate_route
from app.services.route_risk_service import (
    get_nearby_flood_risks,
    get_nearby_emergencies,
    get_nearby_incidents
)
from app.services.traffic_service import get_traffic
from app.database.database import get_db


router = APIRouter(
    prefix="/routing",
    tags=["Routing"]
)

def sample_route_points(route_points, number_of_samples=3):
    if not route_points:
        return []

    if len(route_points) <= number_of_samples:
        return route_points

    indexes = [
        round(
            i * (len(route_points) - 1)
            / (number_of_samples - 1)
        )
        for i in range(number_of_samples)
    ]

    return [
        route_points[index]
        for index in indexes
    ]

def calculate_route_intelligence(
    traffic_data,
    flood_risks,
    nearby_emergencies,
    nearby_incidents
):
    risk_flags = []

    # -----------------------------------
    # Traffic assessment
    # -----------------------------------
    traffic_level = traffic_data.get(
        "congestion_level",
        "UNKNOWN"
    )

    if traffic_level == "SEVERE":
        risk_flags.append("SEVERE_TRAFFIC")

    elif traffic_level == "HIGH":
        risk_flags.append("HIGH_TRAFFIC")

    elif traffic_level == "MODERATE":
        risk_flags.append("MODERATE_TRAFFIC")

    # -----------------------------------
    # Road closure assessment
    # -----------------------------------
    if traffic_data.get("road_closure"):
        risk_flags.append("ROAD_CLOSURE")

    # -----------------------------------
    # Flood assessment
    # -----------------------------------
    if not flood_risks:
        flood_status = "NO_CURRENT_DATA"

    else:
        flood_levels = [
            item["flood_risk"]["risk_level"]
            for item in flood_risks
            if item.get("flood_risk")
        ]

        if "CRITICAL" in flood_levels:
            flood_status = "CRITICAL"
            risk_flags.append("CRITICAL_FLOOD_RISK")

        elif "HIGH" in flood_levels:
            flood_status = "HIGH"
            risk_flags.append("HIGH_FLOOD_RISK")

        elif "MODERATE" in flood_levels:
            flood_status = "MODERATE"
            risk_flags.append("MODERATE_FLOOD_RISK")

        else:
            flood_status = "LOW"

    # -----------------------------------
    # Emergency assessment
    # -----------------------------------
    along_route_emergencies = [
        emergency
        for emergency in nearby_emergencies
        if emergency["location_type"] == "ALONG_ROUTE"
    ]

    emergency_count = len(
        along_route_emergencies
    )

    if emergency_count > 0:
        risk_flags.append("ACTIVE_EMERGENCY_NEAR_ROUTE")

    incident_count = len(nearby_incidents)

    if incident_count > 0:
        risk_flags.append("ACTIVE_INCIDENT_NEAR_ROUTE")


    # -----------------------------------
    # Overall status
    # -----------------------------------
    if (
        "ROAD_CLOSURE" in risk_flags
        or "CRITICAL_FLOOD_RISK" in risk_flags
        or "SEVERE_TRAFFIC" in risk_flags
    ):
        overall_status = "HIGH_RISK"

    elif (
        "HIGH_FLOOD_RISK" in risk_flags
        or "HIGH_TRAFFIC" in risk_flags
        or "MODERATE_FLOOD_RISK" in risk_flags
        or "MODERATE_TRAFFIC" in risk_flags
        or "ACTIVE_EMERGENCY_NEAR_ROUTE" in risk_flags
        or "ACTIVE_INCIDENT_NEAR_ROUTE" in risk_flags

    ):
        overall_status = "MODERATE_RISK"

    elif flood_status == "NO_CURRENT_DATA":
        overall_status = "INSUFFICIENT_DATA"

    else:
        overall_status = "LOW_RISK"

    return {
        "overall_status": overall_status,
        "traffic_status": traffic_level,
        "flood_status": flood_status,
        "road_closure": traffic_data.get(
            "road_closure",
            False
        ),
        "active_emergency_count": emergency_count,
        "active_incident_count": incident_count,
        "origin_emergency_count": len([
            emergency
            for emergency in nearby_emergencies
            if emergency["location_type"] == "ORIGIN"
        ]),
        "risk_flags": risk_flags
    }

def select_recommended_route(analyzed_routes):
    if not analyzed_routes:
        return None

    risk_priority = {
        "LOW_RISK": 0,
        "MODERATE_RISK": 1,
        "INSUFFICIENT_DATA": 2,
        "HIGH_RISK": 3
    }

    def route_score(route):
        intelligence = route["route_intelligence"]

        risk_score = risk_priority.get(
            intelligence["overall_status"],
            100
        )

        congestion = route["traffic"].get(
            "congestion_percentage"
        )

        if congestion is None:
            congestion = 100

        travel_time = route.get(
            "travel_time_minutes",
            999
        )

        distance = route.get(
            "distance_km",
            999
        )

        return (
            risk_score
            + congestion
            + travel_time
            + distance
        )

    recommended_route = min(
        analyzed_routes,
        key=route_score
    )

        # -----------------------------------
    # Calculate normalized 0–100 scores
    # -----------------------------------

    route_scores = {}

    max_congestion = max(
        (
            route["traffic"].get("congestion_percentage") or 100
            for route in analyzed_routes
        ),
        default=100
    )

    max_travel_time = max(
        (
            route.get("travel_time_minutes", 999)
            for route in analyzed_routes
        ),
        default=999
    )

    max_distance = max(
        (
            route.get("distance_km", 999)
            for route in analyzed_routes
        ),
        default=999
    )

    for route in analyzed_routes:
        intelligence = route["route_intelligence"]

        risk = risk_priority.get(
            intelligence["overall_status"],
            3
        )

        risk_score = max(
            0,
            100 - (risk * 25)
        )

        congestion = route["traffic"].get(
            "congestion_percentage"
        )

        if congestion is None:
            congestion = max_congestion

        congestion_score = (
            100
            if max_congestion == 0
            else 100 - (
                congestion / max_congestion * 100
            )
        )

        travel_time = route.get(
            "travel_time_minutes",
            max_travel_time
        )

        travel_time_score = (
            100
            if max_travel_time == 0
            else 100 - (
                travel_time / max_travel_time * 100
            )
        )

        distance = route.get(
            "distance_km",
            max_distance
        )

        distance_score = (
            100
            if max_distance == 0
            else 100 - (
                distance / max_distance * 100
            )
        )

        final_score = (
            risk_score * 0.40
            + congestion_score * 0.30
            + travel_time_score * 0.20
            + distance_score * 0.10
        )

        route_scores[route["route_id"]] = round(
            final_score,
            2
        )

        route["recommendation_score"] = route_scores[
            route["route_id"]
        ]

    recommended_route = max(
        analyzed_routes,
        key=lambda route: route_scores[route["route_id"]]
    )

    recommended_route["recommendation_score"] = route_scores[
        recommended_route["route_id"]
    ]

    return recommended_route

def evaluate_dynamic_rerouting(
    current_route,
    alternative_routes
):
    if not current_route or not alternative_routes:
        return {
            "reroute_required": False,
            "reason": "No alternative route available"
        }

    current_score = current_route.get(
        "recommendation_score",
        0
    )

    best_alternative = max(
        alternative_routes,
        key=lambda route: route.get(
            "recommendation_score",
            0
        )
    )

    alternative_score = best_alternative.get(
        "recommendation_score",
        0
    )

    current_risk = current_route[
        "route_intelligence"
    ]["overall_status"]

    if current_risk == "HIGH_RISK":
        return {
            "reroute_required": True,
            "reason": "Current route has high assessed risk",
            "recommended_route_id": best_alternative["route_id"]
        }

    if alternative_score >= current_score + 10:
        return {
            "reroute_required": True,
            "reason": (
                "Alternative route has significantly "
                "better CityLens recommendation score"
            ),
            "recommended_route_id": best_alternative["route_id"]
        }

    return {
        "reroute_required": False,
        "reason": "Current route remains the best available option",
        "recommended_route_id": current_route["route_id"]
    }

def route_score(route):
    intelligence = route["route_intelligence"]

    risk_score = {
        "LOW_RISK": 0,
        "MODERATE_RISK": 30,
        "INSUFFICIENT_DATA": 50,
        "HIGH_RISK": 100
    }.get(
        intelligence["overall_status"],
        100
    )

    congestion = route["traffic"].get("congestion_percentage")
    if congestion is None:
        congestion = 100

    travel_time = route.get("travel_time_minutes", 999)
    distance = route.get("distance_km", 999)

    return (
        risk_score
        + congestion
        + travel_time
        + distance
    )
    return min(analyzed_routes, key=route_score)

@router.get("/test")
async def test_route(
    origin_latitude: float = Query(...),
    origin_longitude: float = Query(...),
    destination_latitude: float = Query(...),
    destination_longitude: float = Query(...)
):
    try:
        route_data = await calculate_route(
            origin_latitude,
            origin_longitude,
            destination_latitude,
            destination_longitude
        )

        route = route_data["routes"][0]
        summary = route["summary"]

        route_points = route["legs"][0]["points"]

        return {
            "origin": {
                "latitude": origin_latitude,
                "longitude": origin_longitude
            },
            "destination": {
                "latitude": destination_latitude,
                "longitude": destination_longitude
            },
            "distance_km": round(
                summary["lengthInMeters"] / 1000,
                2
            ),
            "travel_time_minutes": round(
                summary["travelTimeInSeconds"] / 60,
                2
            ),
            "traffic_delay_minutes": round(
                summary.get(
                    "trafficDelayInSeconds", 0
                ) / 60,
                2
            ),
            "route": [
                {
                    "latitude": point["latitude"],
                    "longitude": point["longitude"]
                }
                for point in route_points
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/analyze")
async def analyze_route(
    origin_latitude: float = Query(...),
    origin_longitude: float = Query(...),
    destination_latitude: float = Query(...),
    destination_longitude: float = Query(...),
    db: Session = Depends(get_db)
):
    try:
        # -----------------------------------
        # 1. Calculate all available routes
        # -----------------------------------
        route_data = await calculate_route(
            origin_latitude,
            origin_longitude,
            destination_latitude,
            destination_longitude
        )

        routes = route_data.get("routes", [])

        if not routes:
            raise ValueError("No routes returned by TomTom")

        analyzed_routes = []

        # -----------------------------------
        # 2. Analyze each route
        # -----------------------------------
        for index, route in enumerate(routes):

            summary = route["summary"]
            route_points = route["legs"][0]["points"]

            # -----------------------------------
            # Route-level traffic delay
            # -----------------------------------
            traffic_delay_minutes = round(
                summary.get(
                    "trafficDelayInSeconds", 0
                ) / 60,
                2
            )

            # -----------------------------------
            # Traffic at route origin
            # -----------------------------------
            # -----------------------------------
            # Get traffic at sampled route points
            # -----------------------------------
            sampled_points = sample_route_points(
                route_points,
                number_of_samples=3
            )

            traffic_samples = []

            for point in sampled_points:
                try:
                    traffic_data = await get_traffic(
                        point["latitude"],
                        point["longitude"]
                    )

                    traffic_samples.append(
                        traffic_data
                    )

                except Exception:
                    continue

            # -----------------------------------
            # Aggregate traffic information
            # -----------------------------------
            if traffic_samples:
                average_congestion = round(
                    sum(
                        item["congestion_percentage"]
                        for item in traffic_samples
                    ) / len(traffic_samples),
                    2
                )

                if average_congestion >= 70:
                    route_congestion_level = "SEVERE"
                elif average_congestion >= 50:
                    route_congestion_level = "HIGH"
                elif average_congestion >= 25:
                    route_congestion_level = "MODERATE"
                else:
                    route_congestion_level = "LOW"

                road_closure = any(
                    item["road_closure"]
                    for item in traffic_samples
                )

                average_current_speed = round(
                    sum(
                        item["current_speed"]
                        for item in traffic_samples
                        if item["current_speed"] is not None
                    ) / len(
                        [
                            item for item in traffic_samples
                            if item["current_speed"] is not None
                        ]
                    ),
                    2
                )

                average_free_flow_speed = round(
                    sum(
                        item["free_flow_speed"]
                        for item in traffic_samples
                        if item["free_flow_speed"] is not None
                    ) / len(
                        [
                            item for item in traffic_samples
                            if item["free_flow_speed"] is not None
                        ]
                    ),
                    2
                )

                confidence_values = [
                    item["confidence"]
                    for item in traffic_samples
                    if item["confidence"] is not None
                ]

                average_confidence = round(
                    sum(confidence_values)
                    / len(confidence_values),
                    2
                ) if confidence_values else None

            else:
                average_congestion = None
                route_congestion_level = "UNKNOWN"
                road_closure = False
                average_current_speed = None
                average_free_flow_speed = None
                average_confidence = None

            # -----------------------------------
            # Flood-risk analysis
            # -----------------------------------
            flood_risks = get_nearby_flood_risks(
                db,
                route_points
            )

            nearby_emergencies = get_nearby_emergencies(
                db,
                route_points
            )

            nearby_incidents = get_nearby_incidents(
                db,
                route_points
            )

            route_intelligence = calculate_route_intelligence(
                traffic_data={
                    "congestion_level": route_congestion_level,
                    "road_closure": road_closure
                },
                flood_risks=flood_risks,
                nearby_emergencies=nearby_emergencies,
                nearby_incidents=nearby_incidents
            )

            # -----------------------------------
            # Route result
            # -----------------------------------
            analyzed_routes.append({
                "route_id": index + 1,

                "distance_km": round(
                    summary["lengthInMeters"] / 1000,
                    2
                ),

                "travel_time_minutes": round(
                    summary["travelTimeInSeconds"] / 60,
                    2
                ),

                "traffic_delay_minutes":
                    traffic_delay_minutes,

                "traffic": {
                    "current_speed": average_current_speed,
                    "free_flow_speed": average_free_flow_speed,
                    "congestion_percentage": average_congestion,
                    "congestion_level": route_congestion_level,
                    "confidence": average_confidence,
                    "road_closure": road_closure,
                    "samples_used": len(traffic_samples)
                },
                
                "flood_risk_points":
                    flood_risks,

                "nearby_emergencies": nearby_emergencies,

                "nearby_incidents": nearby_incidents,
                
                "route_intelligence":
                    route_intelligence,

                "route_geometry": [
                    {
                        "latitude": point["latitude"],
                        "longitude": point["longitude"]
                    }
                    for point in route_points
                ]
            })

        # -----------------------------------
        # 3. Select recommended route
        # -----------------------------------

        recommended_route = select_recommended_route(
            analyzed_routes
        )

        alternative_routes = [
            route
            for route in analyzed_routes
            if route["route_id"] != recommended_route["route_id"]
        ]

        rerouting_analysis = evaluate_dynamic_rerouting(
            recommended_route,
            alternative_routes
        )

        recommendation = None

        if recommended_route:
            recommendation = {
                "route_id": recommended_route["route_id"],
                "score": recommended_route["recommendation_score"],
                "reason": (
                    "Recommended based on the lowest assessed route risk, "
                    "traffic congestion, travel time, and distance."
                ),
                "factors": {
                    "risk": recommended_route["route_intelligence"]["overall_status"],
                    "congestion": f'{recommended_route["traffic"]["congestion_percentage"]}%',
                    "travel_time_minutes": recommended_route["travel_time_minutes"],
                    "road_closure": recommended_route["traffic"]["road_closure"],
                    "flood_data_available": (
                        recommended_route["route_intelligence"]["flood_status"]
                        != "NO_CURRENT_DATA"
                    ),
                    "active_emergencies_along_route": (
                        recommended_route["route_intelligence"]["active_emergency_count"]
                    ),
                    "active_incidents_along_route": (
                        recommended_route["route_intelligence"]["active_incident_count"]
                    ),
                },
                "summary": (
                    f"Route {recommended_route['route_id']} is currently the best available option "
                    f"with {recommended_route['traffic']['congestion_percentage']}% congestion "
                    f"and an estimated travel time of "
                    f"{recommended_route['travel_time_minutes']} minutes. "
                    "Flood-risk data is currently unavailable for this route."
                )
            }
        # -----------------------------------
        # 4. Return all analyzed routes
        # -----------------------------------

        return {
            "origin": {
                "latitude": origin_latitude,
                "longitude": origin_longitude
            },

            "destination": {
                "latitude": destination_latitude,
                "longitude": destination_longitude
            },

            "recommended_route_id": (
                recommended_route["route_id"]
                if recommended_route
                else None
            ),

            "recommendation": recommendation,

            "dynamic_rerouting": rerouting_analysis,

            "routes": analyzed_routes
            
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
