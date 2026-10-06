from pydantic import BaseModel


class AQIResponse(BaseModel):
    city: str
    timestamp: str
    pm10: float
    pm2_5: float
    carbon_monoxide: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    ozone: float
    european_aqi: float
    us_aqi: float