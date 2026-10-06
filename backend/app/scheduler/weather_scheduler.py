from datetime import datetime, timedelta
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.weather_service import get_weather_for_locations
from app.database.database import SessionLocal
from app.models.weather import WeatherData
from app.models.location import Location

scheduler = AsyncIOScheduler()

BATCH_SIZE = 50


async def collect_weather():
    db = SessionLocal()

    try:
        # Only collect weather for locations that do not
        # already have a recent weather record.
        cutoff_time = (
            datetime.now().astimezone()
            - timedelta(minutes=14)
        )

        recent_location_ids = (
            db.query(WeatherData.location_id)
            .filter(
                WeatherData.location_id.isnot(None),
                WeatherData.timestamp >= cutoff_time
            )
            .distinct()
            .all()
        )

        recent_location_ids = {
            row[0]
            for row in recent_location_ids
        }

        locations = (
            db.query(Location)
            .filter(
                Location.is_active == True,
                ~Location.id.in_(recent_location_ids)
            )
            .order_by(Location.id)
            .all()
        )

        print(
            f"Starting weather collection for "
            f"{len(locations)} locations..."
        )

        print(
            f"Skipping {len(recent_location_ids)} "
            f"locations with recent weather data."
        )

        successful = 0
        failed = 0

        for start in range(0, len(locations), BATCH_SIZE):

            # Small delay between API batches
            await asyncio.sleep(2)

            batch = locations[
                start:start + BATCH_SIZE
            ]

            print(
                f"Fetching batch "
                f"{start + 1}-"
                f"{start + len(batch)}..."
            )

            try:
                max_retries = 3
                weather_results = None

                for attempt in range(max_retries):

                    try:
                        weather_results = (
                            await get_weather_for_locations(
                                batch
                            )
                        )

                        break

                    except Exception as e:

                        if (
                            "429" in str(e)
                            and attempt < max_retries - 1
                        ):
                            wait_time = 10 * (attempt + 1)

                            print(
                                f"Rate limited. "
                                f"Waiting {wait_time} "
                                f"seconds before retry..."
                            )

                            await asyncio.sleep(
                                wait_time
                            )

                        else:
                            raise

                if isinstance(
                    weather_results,
                    dict
                ):
                    weather_results = [
                        weather_results
                    ]

                for location, weather_data in zip(
                    batch,
                    weather_results
                ):

                    current = weather_data["current"]

                    weather_record = WeatherData(
                        timestamp=datetime.fromisoformat(
                            current["time"]
                        ),
                        temperature=current[
                            "temperature_2m"
                        ],
                        apparent_temperature=current[
                            "apparent_temperature"
                        ],
                        humidity=current[
                            "relative_humidity_2m"
                        ],
                        precipitation=current[
                            "precipitation"
                        ],
                        rain=current["rain"],
                        weather_code=current[
                            "weather_code"
                        ],
                        wind_speed=current[
                            "wind_speed_10m"
                        ],
                        latitude=location.latitude,
                        longitude=location.longitude,
                        location_id=location.id
                    )

                    db.add(weather_record)

                    successful += 1

            except Exception as e:

                failed += len(batch)

                print(
                    f"Batch failed "
                    f"{start + 1}-"
                    f"{start + len(batch)}: {e}"
                )

        db.commit()

        print(
            f"Weather collection completed. "
            f"Successful: {successful}, "
            f"Failed: {failed}"
        )

    except Exception as e:

        db.rollback()

        print(
            "Weather collection failed:",
            e
        )

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