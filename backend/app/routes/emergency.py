from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.emergency import Emergency
from app.schemas.emergency import EmergencyCreate, EmergencyResponse, EmergencyWithRecommendationResponse
from app.models.user import User
from app.security.auth import get_current_user, require_role
from app.websocket.manager import manager
from app.ai.resource_recommendation import recommend_resources
from app.services.flood_risk_service import calculate_flood_risk
from app.models.bmc_weather import BMCWeatherData
from app.models.incident_report import IncidentReport
from app.services.traffic_service import get_traffic

router = APIRouter(
    prefix="/emergencies",
    tags=["Emergencies"]
)


@router.post(
    "",
    response_model=EmergencyWithRecommendationResponse

)
async def create_emergency(
    emergency_data: EmergencyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_emergency = Emergency(
        user_id=current_user.id,
        emergency_type=emergency_data.emergency_type,
        description=emergency_data.description,
        latitude=emergency_data.latitude,
        longitude=emergency_data.longitude,
        status="active"
    )

    stations = db.query(BMCWeatherData).all()

    nearest_station = None
    nearest_distance = None

    for station in stations:
        distance = (
            (station.latitude - emergency_data.latitude) ** 2
            + (station.longitude - emergency_data.longitude) ** 2
        )

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_station = station

    flood_risk = "LOW"

    if nearest_station:
        flood_analysis = calculate_flood_risk(
            db,
            nearest_station.bmc_location_id
        )



        if flood_analysis:
            flood_risk = flood_analysis["risk_level"]

    nearby_incidents = (
        db.query(IncidentReport)
        .filter(
            IncidentReport.status.in_(
                ["verified", "investigating"]
            )
        )
        .all()
    )

    nearby_incident_count = 0

    for incident in nearby_incidents:
        distance = (
            (incident.latitude - emergency_data.latitude) ** 2
            + (incident.longitude - emergency_data.longitude) ** 2
        )

        if distance <= 0.005 ** 2:
            nearby_incident_count += 1

    traffic_analysis = await get_traffic(
        emergency_data.latitude,
        emergency_data.longitude
    )

    traffic_level = traffic_analysis["congestion_level"]

    resource_recommendation = recommend_resources(
        emergency_type=emergency_data.emergency_type,
        flood_risk=flood_risk,
        traffic_level=traffic_level,
        incident_count=nearby_incident_count
    )

    db.add(new_emergency)
    db.commit()
    db.refresh(new_emergency)

    await manager.broadcast({
        "event": "new_emergency",
        "emergency": {
            "id": new_emergency.id,
            "user_id": new_emergency.user_id,
            "emergency_type": new_emergency.emergency_type,
            "description": new_emergency.description,
            "latitude": new_emergency.latitude,
            "longitude": new_emergency.longitude,
            "status": new_emergency.status
        }
    })

    return {
        "emergency": new_emergency,
        "resource_recommendation": resource_recommendation
    }

@router.get(
    "",
    response_model=list[EmergencyResponse]
)
def get_emergencies(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    emergencies = (
        db.query(Emergency)
        .order_by(Emergency.created_at.desc())
        .all()
    )

    return emergencies

@router.patch("/{emergency_id}/status")

async def update_emergency_status(
    emergency_id: int,
    status: str,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    emergency = (
        db.query(Emergency)
        .filter(Emergency.id == emergency_id)
        .first()
    )

    if emergency is None:
        raise HTTPException(
            status_code=404,
            detail="Emergency not found"
        )

    allowed_statuses = {
        "active",
        "dispatched",
        "resolved"
    }

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid emergency status"
        )

    emergency.status = status

    db.commit()
    db.refresh(emergency)

    await manager.broadcast({
        "event": "emergency_status_updated",
        "emergency": {
            "id": emergency.id,
            "user_id": emergency.user_id,
            "emergency_type": emergency.emergency_type,
            "description": emergency.description,
            "latitude": emergency.latitude,
            "longitude": emergency.longitude,
            "status": emergency.status
        }
    })

    return emergency