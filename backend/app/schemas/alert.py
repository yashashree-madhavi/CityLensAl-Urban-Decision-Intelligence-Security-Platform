from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    user_id: Optional[int]
    alert_type: str
    title: str
    message: str
    severity: str
    is_read: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True