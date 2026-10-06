from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.flood_risk_service import calculate_flood_risk
from app.models.bmc_weather import BMCWeatherData

router = APIRouter(
    prefix="/flood-risk",
    tags=["Flood Risk"]
)

@router.get("")
def get_all_flood_risks(
    db: Session = Depends(get_db)
):
    results = (
        db.query(BMCWeatherData)
        .order_by(
            BMCWeatherData.bmc_location_id,
            BMCWeatherData.timestamp.desc()
        )
        .all()
    )

    latest_by_station = {}

    for weather in results:
        if weather.bmc_location_id not in latest_by_station:
            latest_by_station[
                weather.bmc_location_id
            ] = weather

    flood_risks = []

    for location_id in latest_by_station:
        risk = calculate_flood_risk(
            db,
            location_id
        )

        if risk:
            flood_risks.append(risk)

    return {
        "total_stations": len(flood_risks),
        "stations": flood_risks
    }

@router.get("/{bmc_location_id}")
def get_flood_risk(
    bmc_location_id: int,
    db: Session = Depends(get_db)
):
    result = calculate_flood_risk(
        db,
        bmc_location_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="BMC weather data not found for this location"
        )

    return result
