from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.weather import WeatherData
from app.models.location import Location
from app.services.weather_service import get_weather, get_weather_for_locations
from app.schemas.weather import WeatherResponse


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get(
    "/current/{location_id}",
    response_model=WeatherResponse
)
async def current_weather(
    location_id: int,
    db: Session = Depends(get_db)
):
    location = (
        db.query(Location)
        .filter(
            Location.id == location_id,
            Location.is_active == True
        )
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found or inactive"
        )

    try:
        weather_data = await get_weather(
            location.latitude,
            location.longitude
        )

        current = weather_data["current"]

        weather_record = WeatherData(
            timestamp=datetime.fromisoformat(
                current["time"]
            ),
            temperature=current["temperature_2m"],
            apparent_temperature=current["apparent_temperature"],
            humidity=current["relative_humidity_2m"],
            precipitation=current["precipitation"],
            rain=current["rain"],
            weather_code=current["weather_code"],
            wind_speed=current["wind_speed_10m"],
            latitude=location.latitude,
            longitude=location.longitude,
            location_id=location.id
        )

        db.add(weather_record)
        db.commit()
        db.refresh(weather_record)

        return {
            "city": location.name,
            "timestamp": current["time"],
            "temperature": current["temperature_2m"],
            "apparent_temperature": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "rain": current["rain"],
            "weather_code": current["weather_code"],
            "wind_speed": current["wind_speed_10m"]
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch and store weather data: {str(e)}"
        )

@router.get("/test-batch")
async def test_batch_weather(
    db: Session = Depends(get_db)
):
    locations = (
        db.query(Location)
        .filter(Location.is_active == True)
        .order_by(Location.id)
        .limit(5)
        .all()
    )

    weather_results = await get_weather_for_locations(locations)

    return {
        "locations_requested": len(locations),
        "weather_results": len(weather_results),
        "data": [
            {
                "location_id": location.id,
                "location": location.name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "weather": weather
            }
            for location, weather in zip(
                locations,
                weather_results
            )
        ]
    }