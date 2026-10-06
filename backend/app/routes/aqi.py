from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.aqi import AQIData
from app.services.aqi_service import get_mumbai_aqi
from app.schemas.aqi import AQIResponse


router = APIRouter(
    prefix="/aqi",
    tags=["AQI"]
)


@router.get(
    "/current",
    response_model=AQIResponse
)
async def current_aqi(
    db: Session = Depends(get_db)
):
    try:
        aqi_data = await get_mumbai_aqi()

        current = aqi_data["current"]

        aqi_record = AQIData(
            timestamp=datetime.fromisoformat(
                current["time"]
            ),
            pm10=current["pm10"],
            pm2_5=current["pm2_5"],
            carbon_monoxide=current["carbon_monoxide"],
            nitrogen_dioxide=current["nitrogen_dioxide"],
            sulphur_dioxide=current["sulphur_dioxide"],
            ozone=current["ozone"],
            european_aqi=current["european_aqi"],
            us_aqi=current["us_aqi"],
            latitude=19.0760,
            longitude=72.8777
        )

        db.add(aqi_record)
        db.commit()
        db.refresh(aqi_record)

        return {
            "city": "Mumbai",
            "timestamp": current["time"],
            "pm10": current["pm10"],
            "pm2_5": current["pm2_5"],
            "carbon_monoxide": current["carbon_monoxide"],
            "nitrogen_dioxide": current["nitrogen_dioxide"],
            "sulphur_dioxide": current["sulphur_dioxide"],
            "ozone": current["ozone"],
            "european_aqi": current["european_aqi"],
            "us_aqi": current["us_aqi"]
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to fetch and store AQI data: {str(e)}"
        )