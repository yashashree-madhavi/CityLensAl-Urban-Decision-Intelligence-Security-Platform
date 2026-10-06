from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database.database import Base


class IncidentReport(Base):
    __tablename__ = "incident_reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    incident_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    status = Column(String(30), nullable=False, default="reported")

    ai_classification = Column(
        String(30),
        nullable=True
    )

    ai_suspicion_score = Column(
        Float,
        nullable=True
    )

    ai_reason = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )