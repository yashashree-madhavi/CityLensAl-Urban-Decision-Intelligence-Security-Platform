from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    alert_type = Column(String(50), nullable=False)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="info")
    is_read = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())