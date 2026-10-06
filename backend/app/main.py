from fastapi import FastAPI, Depends
from sqlalchemy import text

from app.models.user import User
from app.models.emergency import Emergency
from app.models.weather import WeatherData
from app.models.aqi import AQIData
from app.models.location import Location
from app.models.incident_report import IncidentReport
from app.models.alert import Alert
from app.database.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.emergency import router as emergency_router
from app.security.auth import get_current_user, require_role
from app.websocket.connection import router as websocket_router
from app.routes.weather import router as weather_router
from app.routes.aqi import router as aqi_router
from app.routes.locations import router as locations_router
from app.routes.bmc_weather import router as bmc_weather_router
from app.routes.flood_risk import router as flood_risk_router
from app.routes.traffic import router as traffic_router
from app.routes.routing import router as routing_router
from app.routes.incidents import router as incidents_router
from app.routes.alerts import router as alerts_router
from app.routes.ml_prediction import router as ml_prediction_router
from app.routes.resource_recommendation import router as resource_recommendation_router
from app.models.bmc_weather import BMCWeatherData
from app.models.traffic import TrafficData
from app.scheduler.weather_scheduler import start_weather_scheduler
from app.scheduler.aqi_scheduler import start_aqi_scheduler
from app.services.bmc_weather_scheduler import (
    start_bmc_weather_scheduler
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CityLens AI",
    description="AI-Powered Urban Decision Intelligence Platform for Mumbai",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(emergency_router)
app.include_router(websocket_router)
app.include_router(weather_router)
app.include_router(aqi_router)
app.include_router(locations_router)
app.include_router(bmc_weather_router)
app.include_router(flood_risk_router)
app.include_router(traffic_router)
app.include_router(routing_router)
app.include_router(incidents_router)
app.include_router(alerts_router)
app.include_router(ml_prediction_router)
app.include_router(resource_recommendation_router)

start_weather_scheduler()
start_aqi_scheduler()
start_bmc_weather_scheduler()

@app.get("/")
def root():
    return {
        "message": "CityLens AI Backend is running 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {
                "database": "connected",
                "result": result.scalar()
            }

    except Exception as e:
        return {
            "database": "connection failed",
            "error": str(e)
        }

@app.get("/protected-test")
def protected_test(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "name": current_user.name,
        "role": current_user.role
    }

@app.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_role("admin"))
):
    return {
        "message": "Welcome Admin!",
        "user_id": current_user.id,
        "name": current_user.name,
        "role": current_user.role
    }