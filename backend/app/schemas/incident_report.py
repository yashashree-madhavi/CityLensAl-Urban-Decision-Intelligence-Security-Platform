from pydantic import BaseModel
from typing import Optional


class IncidentReportCreate(BaseModel):
    incident_type: str
    description: Optional[str] = None
    latitude: float
    longitude: float


class IncidentReportResponse(BaseModel):
    id: int
    user_id: int
    incident_type: str
    description: Optional[str]
    latitude: float
    longitude: float
    status: str

    ai_classification: Optional[str] = None
    ai_suspicion_score: Optional[float] = None
    ai_reason: Optional[str] = None

    class Config:
        from_attributes = True