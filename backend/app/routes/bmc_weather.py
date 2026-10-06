from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.bmc_weather_service import (
    get_bmc_weather,
    collect_all_bmc_weather
)


router = APIRouter(
    prefix="/bmc-weather",
    tags=["BMC Weather"]
)


@router.get("/{location_id}")
async def get_bmc_weather_data(
    location_id: int
):
    try:
        return await get_bmc_weather(
            location_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"BMC weather service error: {str(e)}"
        )


@router.post("/collect")
async def collect_bmc_weather(
    db: Session = Depends(get_db)
):
    try:
        return await collect_all_bmc_weather(
            db
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"BMC collection failed: {str(e)}"
        )