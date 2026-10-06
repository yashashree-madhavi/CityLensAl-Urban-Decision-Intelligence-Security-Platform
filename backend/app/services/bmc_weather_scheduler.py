from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.database import SessionLocal
from app.services.bmc_weather_service import collect_all_bmc_weather


scheduler = AsyncIOScheduler()


async def collect_bmc_weather_job():
    db = SessionLocal()

    try:
        result = await collect_all_bmc_weather(db)

        print(
            "BMC weather job completed:",
            result
        )

    except Exception as e:
        db.rollback()

        print(
            "BMC weather job failed:",
            e
        )

    finally:
        db.close()


def start_bmc_weather_scheduler():

    scheduler.add_job(
        collect_bmc_weather_job,
        "interval",
        minutes=15,
        id="bmc_weather_collection",
        replace_existing=True
    )

    scheduler.start()

    print(
        "BMC weather scheduler started. "
        "Collecting every 15 minutes."
    )