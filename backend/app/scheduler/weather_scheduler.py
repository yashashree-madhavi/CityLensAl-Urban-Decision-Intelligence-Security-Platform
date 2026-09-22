from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.weather_service import get_mumbai_weather
from app.database.database import SessionLocal
from app.models.weather import WeatherData


scheduler = AsyncIOScheduler()


async def collect_weather():
    db = SessionLocal()

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

        print(
            "Weather collected and stored:",
            current
        )

    except Exception as e:
        db.rollback()
        print("Weather collection failed:", e)

    finally:
        db.close()


def start_weather_scheduler():
    scheduler.add_job(
        collect_weather,
        "interval",
        minutes=15,
        id="mumbai_weather_collection",
        replace_existing=True
    )

    scheduler.start()

    print(
        "Weather scheduler started. "
        "Collecting every 15 minutes."
    )