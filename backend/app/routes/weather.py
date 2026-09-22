from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.weather import WeatherData
from app.services.weather_service import get_mumbai_weather
from app.schemas.weather import WeatherResponse


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get(
    "/current",
    response_model=WeatherResponse
)
async def current_weather(
    db: Session = Depends(get_db)
):
    try:
        weather_data = await get_mumbai_weather()

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
            latitude=19.0760,
            longitude=72.8777
        )

        db.add(weather_record)
        db.commit()
        db.refresh(weather_record)

        return {
            "city": "Mumbai",
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