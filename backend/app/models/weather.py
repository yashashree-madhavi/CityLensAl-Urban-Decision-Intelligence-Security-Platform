from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=True
    )

    apparent_temperature = Column(
        Float,
        nullable=True
    )

    humidity = Column(
        Float,
        nullable=True
    )

    precipitation = Column(
        Float,
        nullable=True
    )

    rain = Column(
        Float,
        nullable=True
    )

    weather_code = Column(
        Integer,
        nullable=True
    )

    wind_speed = Column(
        Float,
        nullable=True
    )

    latitude = Column(
        Float,
        nullable=False
    )

    longitude = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )