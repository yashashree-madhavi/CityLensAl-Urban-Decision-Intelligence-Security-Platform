from fastapi import APIRouter
from app.ai.resource_recommendation import recommend_resources

router = APIRouter(
    prefix="/ai",
    tags=["AI Intelligence"]
)


@router.post("/resource-recommendation")
def resource_recommendation(
    emergency_type: str,
    flood_risk: str = "LOW",
    traffic_level: str = "LOW",
    incident_count: int = 0
):
    return recommend_resources(
        emergency_type=emergency_type,
        flood_risk=flood_risk,
        traffic_level=traffic_level,
        incident_count=incident_count
    )