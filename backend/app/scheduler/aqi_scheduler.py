from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.aqi_service import get_mumbai_aqi
from app.database.database import SessionLocal
from app.models.aqi import AQIData


scheduler = AsyncIOScheduler()


async def collect_aqi():
    db = SessionLocal()

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

        print(
            "AQI collected and stored:",
            current
        )

    except Exception as e:
        db.rollback()
        print("AQI collection failed:", e)

    finally:
        db.close()


def start_aqi_scheduler():
    scheduler.add_job(
        collect_aqi,
        "interval",
        minutes=15,
        id="mumbai_aqi_collection",
        replace_existing=True
    )

    scheduler.start()

    print(
        "AQI scheduler started. "
        "Collecting every 15 minutes."
    )