import httpx
from datetime import datetime

from app.models.bmc_weather import BMCWeatherData


BMC_SUBLOCATION_URL = (
    "https://dmwebtwo.mcgm.gov.in/"
    "api/sublocation/loadAll"
)

BMC_WEATHER_URL = (
    "https://dmwebtwo.mcgm.gov.in/"
    "api/tabWeatherForecastData/loadById"
)


async def get_bmc_weather(location_id: int):
    """
    Fetch live weather data for one BMC AWS station.
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            BMC_WEATHER_URL,
            json={"id": location_id},
            timeout=15.0
        )

        response.raise_for_status()

        data = response.json()

    location = data.get("locationList", {})
    weather = data.get(
        "dummyTestRaingaugeDataDetails",
        {}
    )

    return {
        "bmc_location_id": location.get("id"),
        "station_name": location.get("description"),
        "latitude": float(location.get("lati")),
        "longitude": float(location.get("longi")),
        "timestamp": weather.get("timerecorded"),

        "temperature": float(
            weather.get("tempOut", 0)
        ),

        "humidity": float(
            weather.get("outHumidity", 0)
        ),

        "wind_speed": float(
            weather.get("windSpeed", 0)
        ),

        "wind_direction": weather.get(
            "windDir"
        ),

        "pressure": float(
            weather.get("bar", 0)
        ),

        "rain_15min": float(
            weather.get("rain", 0)
        ),

        "rain_rate": float(
            weather.get("rainRate", 0)
        ),

        "rain_1hr": float(
            data.get("avgRainOneHourAWS", 0)
        ),

        "rain_3hr": float(
            data.get("avgRainThreeHourAWS", 0)
        ),

        "rain_6hr": float(
            data.get("avgRainSixHourAWS", 0)
        ),

        "rain_12hr": float(
            data.get("avgRainTwelveHourAWS", 0)
        ),

        "rain_24hr": float(
            data.get("avgRainTwentyFourHourAWS", 0)
        ),
    }


async def get_bmc_location_ids():
    """
    Get all unique BMC AWS location IDs.
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            BMC_SUBLOCATION_URL,
            json={},
            timeout=15.0
        )

        response.raise_for_status()

        locations = response.json()

    location_ids = sorted(
        {
            item["locationid"]
            for item in locations
            if item.get("locationid") is not None
        }
    )

    return location_ids


async def collect_all_bmc_weather(db):
    """
    Collect current weather data from all BMC AWS stations
    and store the observations in PostgreSQL.
    """

    location_ids = await get_bmc_location_ids()

    print(
        f"Starting BMC weather collection for "
        f"{len(location_ids)} AWS stations..."
    )

    successful = 0
    failed = 0

    async with httpx.AsyncClient() as client:

        for location_id in location_ids:

            try:
                response = await client.post(
                    BMC_WEATHER_URL,
                    json={"id": location_id},
                    timeout=15.0
                )

                response.raise_for_status()

                data = response.json()

                location = data.get(
                    "locationList",
                    {}
                )

                weather = data.get(
                    "dummyTestRaingaugeDataDetails",
                    {}
                )

                timestamp = weather.get(
                    "timerecorded"
                )

                if not timestamp:
                    raise ValueError(
                        "Missing BMC weather timestamp"
                    )

                weather_record = BMCWeatherData(
                    bmc_location_id=location.get(
                        "id"
                    ),

                    station_name=location.get(
                        "description"
                    ),

                    latitude=float(
                        location.get("lati")
                    ),

                    longitude=float(
                        location.get("longi")
                    ),

                    timestamp=datetime.strptime(
                        timestamp.split(".")[0],
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    temperature=float(
                        weather.get(
                            "tempOut", 0
                        )
                    ),

                    humidity=float(
                        weather.get(
                            "outHumidity", 0
                        )
                    ),

                    wind_speed=float(
                        weather.get(
                            "windSpeed", 0
                        )
                    ),

                    wind_direction=weather.get(
                        "windDir"
                    ),

                    pressure=float(
                        weather.get(
                            "bar", 0
                        )
                    ),

                    rain_15min=float(
                        weather.get(
                            "rain", 0
                        )
                    ),

                    rain_rate=float(
                        weather.get(
                            "rainRate", 0
                        )
                    ),

                    rain_1hr=float(
                        data.get(
                            "avgRainOneHourAWS",
                            0
                        )
                    ),

                    rain_3hr=float(
                        data.get(
                            "avgRainThreeHourAWS",
                            0
                        )
                    ),

                    rain_6hr=float(
                        data.get(
                            "avgRainSixHourAWS",
                            0
                        )
                    ),

                    rain_12hr=float(
                        data.get(
                            "avgRainTwelveHourAWS",
                            0
                        )
                    ),

                    rain_24hr=float(
                        data.get(
                            "avgRainTwentyFourHourAWS",
                            0
                        )
                    ),
                )

                db.add(weather_record)

                successful += 1

            except Exception as e:

                failed += 1

                print(
                    f"BMC station {location_id} "
                    f"failed: {e}"
                )

    db.commit()

    print(
        f"BMC weather collection completed. "
        f"Successful: {successful}, "
        f"Failed: {failed}"
    )

    return {
        "total_stations": len(location_ids),
        "successful": successful,
        "failed": failed
    }