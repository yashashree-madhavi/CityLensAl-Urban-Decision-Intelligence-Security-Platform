from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class AQIData(Base):
    __tablename__ = "aqi_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False
    )

    pm10 = Column(
        Float,
        nullable=True
    )

    pm2_5 = Column(
        Float,
        nullable=True
    )

    carbon_monoxide = Column(
        Float,
        nullable=True
    )

    nitrogen_dioxide = Column(
        Float,
        nullable=True
    )

    sulphur_dioxide = Column(
        Float,
        nullable=True
    )

    ozone = Column(
        Float,
        nullable=True
    )

    european_aqi = Column(
        Float,
        nullable=True
    )

    us_aqi = Column(
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