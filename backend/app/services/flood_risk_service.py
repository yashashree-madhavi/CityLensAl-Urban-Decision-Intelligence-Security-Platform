from datetime import datetime

from sqlalchemy.orm import Session

from app.models.bmc_weather import BMCWeatherData
from app.ai.flood_prediction import predict_heavy_rain


def calculate_flood_risk(
    db: Session,
    bmc_location_id: int
):
    """
    Calculate an explainable flood-risk score
    using the latest BMC AWS observation
    and the CityLens heavy-rainfall ML model.
    """

    weather = (
        db.query(BMCWeatherData)
        .filter(
            BMCWeatherData.bmc_location_id
            == bmc_location_id
        )
        .order_by(
            BMCWeatherData.timestamp.desc()
        )
        .first()
    )

    if not weather:
        return None

    score = 0
    reasons = []

    # -----------------------------
    # Data freshness
    # -----------------------------

    now = datetime.now().astimezone()

    weather_timestamp = weather.timestamp

    if weather_timestamp.tzinfo is None:
        weather_timestamp = weather_timestamp.replace(
            tzinfo=now.tzinfo
        )

    data_age_minutes = (
        now - weather_timestamp
    ).total_seconds() / 60

    if data_age_minutes <= 30:
        data_status = "FRESH"

    elif data_age_minutes <= 90:
        data_status = "STALE"

    else:
        data_status = "UNAVAILABLE"

    # -----------------------------
    # 15-minute rainfall
    # -----------------------------

    rain_15min = weather.rain_15min or 0

    if rain_15min >= 20:
        score += 35
        reasons.append(
            "Very high short-term rainfall"
        )

    elif rain_15min >= 10:
        score += 25
        reasons.append(
            "High short-term rainfall"
        )

    elif rain_15min >= 5:
        score += 15
        reasons.append(
            "Moderate short-term rainfall"
        )

    else:
        reasons.append(
            "Low short-term rainfall"
        )

    # -----------------------------
    # 1-hour rainfall
    # -----------------------------

    rain_1hr = weather.rain_1hr or 0

    if rain_1hr >= 50:
        score += 30
        reasons.append(
            "Very high 1-hour rainfall"
        )

    elif rain_1hr >= 30:
        score += 20
        reasons.append(
            "High 1-hour rainfall"
        )

    elif rain_1hr >= 15:
        score += 10
        reasons.append(
            "Moderate 1-hour rainfall"
        )

    # -----------------------------
    # 3-hour rainfall
    # -----------------------------

    rain_3hr = weather.rain_3hr or 0

    if rain_3hr >= 100:
        score += 25
        reasons.append(
            "Very high 3-hour rainfall accumulation"
        )

    elif rain_3hr >= 70:
        score += 20
        reasons.append(
            "High 3-hour rainfall accumulation"
        )

    elif rain_3hr >= 30:
        score += 10
        reasons.append(
            "Moderate 3-hour rainfall accumulation"
        )

    # -----------------------------
    # 24-hour rainfall
    # -----------------------------

    rain_24hr = weather.rain_24hr or 0

    if rain_24hr >= 120:
        score += 20
        reasons.append(
            "Very high 24-hour rainfall accumulation"
        )

    elif rain_24hr >= 70:
        score += 15
        reasons.append(
            "High 24-hour rainfall accumulation"
        )

    elif rain_24hr >= 30:
        score += 10
        reasons.append(
            "Moderate 24-hour rainfall accumulation"
        )

    elif rain_24hr > 0:
        reasons.append(
            f"Low 24-hour rainfall accumulation ({rain_24hr} mm)"
        )

    else:
        reasons.append(
            "No significant 24-hour rainfall accumulation"
        )

    # -----------------------------
    # Base risk level
    # -----------------------------

    if data_status == "UNAVAILABLE":
        risk_level = "UNAVAILABLE"

        reasons = [
            "Current BMC weather data is unavailable"
        ]

    else:
        score = min(score, 100)

        if score >= 70:
            risk_level = "CRITICAL"

        elif score >= 50:
            risk_level = "HIGH"

        elif score >= 25:
            risk_level = "MODERATE"

        else:
            risk_level = "LOW"

    # -----------------------------
    # ML heavy-rain prediction
    # -----------------------------

    ml_prediction = None

    if data_status != "UNAVAILABLE":
        ml_prediction = predict_heavy_rain({
            "month": now.month,
            "day_of_year": now.timetuple().tm_yday,
            "rainfall_previous_day": rain_24hr,
            "rainfall_3day": rain_3hr,
            "rainfall_7day": rain_24hr
        })

        if ml_prediction["prediction"] == "HIGH":
            reasons.append(
                "ML model predicts a high probability "
                "of heavy rainfall"
            )

            if risk_level == "LOW":
                risk_level = "MODERATE"

            elif risk_level == "MODERATE":
                risk_level = "HIGH"

    # -----------------------------
    # Final response
    # -----------------------------

    return {
        "bmc_location_id": weather.bmc_location_id,
        "station_name": weather.station_name,
        "latitude": weather.latitude,
        "longitude": weather.longitude,
        "timestamp": weather.timestamp,
        "data_status": data_status,
        "data_age_minutes": round(
            max(data_age_minutes, 0),
            1
        ),
        "risk_score": score,
        "risk_level": risk_level,
        "ml_prediction": ml_prediction,
        "rainfall": {
            "rain_15min": rain_15min,
            "rain_1hr": rain_1hr,
            "rain_3hr": rain_3hr,
            "rain_24hr": rain_24hr
        },
        "reasons": reasons
    }