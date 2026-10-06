from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class TrafficData(Base):
    __tablename__ = "traffic_data"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(
        Integer,
        ForeignKey("locations.id"),
        nullable=True,
        index=True
    )

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    current_speed = Column(Float, nullable=True)
    free_flow_speed = Column(Float, nullable=True)

    current_travel_time = Column(Float, nullable=True)
    free_flow_travel_time = Column(Float, nullable=True)

    confidence = Column(Float, nullable=True)

    road_closure = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )