from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    timestamp: str
    temperature: float
    apparent_temperature: float
    humidity: float
    precipitation: float
    rain: float
    weather_code: int
    wind_speed: float