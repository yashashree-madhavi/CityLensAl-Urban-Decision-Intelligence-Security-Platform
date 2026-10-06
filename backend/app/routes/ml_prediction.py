from fastapi import APIRouter
from app.ai.flood_prediction import predict_heavy_rain

router = APIRouter(
    prefix="/ml",
    tags=["ML Prediction"]
)


@router.post("/flood-prediction")
def flood_prediction(
    month: int,
    day_of_year: int,
    rainfall_previous_day: float,
    rainfall_3day: float,
    rainfall_7day: float
):
    prediction = predict_heavy_rain({
        "month": month,
        "day_of_year": day_of_year,
        "rainfall_previous_day": rainfall_previous_day,
        "rainfall_3day": rainfall_3day,
        "rainfall_7day": rainfall_7day
    })

    return {
        "model": "Mumbai Heavy Rainfall Prediction",
        "prediction": prediction
    }