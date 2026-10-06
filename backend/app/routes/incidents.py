from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.incident_report import IncidentReport
from app.models.alert import Alert
from app.schemas.incident_report import (
    IncidentReportCreate,
    IncidentReportResponse
)
from app.models.user import User
from app.security.auth import get_current_user
from app.security.auth import require_role
from app.ai.fake_report_detection import detect_suspicious_report

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post(
    "",
    response_model=IncidentReportResponse,
    status_code=201
)
def create_incident(
    incident: IncidentReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_incidents = (
        db.query(IncidentReport)
        .filter(
            IncidentReport.status != "rejected"
        )
        .all()
    )
        
    new_incident = IncidentReport(
        user_id=current_user.id,
        incident_type=incident.incident_type,
        description=incident.description,
        latitude=incident.latitude,
        longitude=incident.longitude,
        status="reported"
    )

    ai_analysis = detect_suspicious_report(
        existing_incidents,
        new_incident
    )

    new_incident.ai_classification = (
        ai_analysis["classification"]
    )

    new_incident.ai_suspicion_score = (
        ai_analysis["suspicion_score"]
    )

    new_incident.ai_reason = (
        ai_analysis["reason"]
    )
    
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get(
    "",
    response_model=list[IncidentReportResponse]
)
def get_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return db.query(IncidentReport).order_by(
        IncidentReport.created_at.desc()
    ).all()

@router.patch("/{incident_id}/status")
def update_incident_status(
    incident_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    allowed_statuses = [
        "reported",
        "verified",
        "investigating",
        "resolved",
        "rejected"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid incident status"
        )

    incident = (
        db.query(IncidentReport)
        .filter(IncidentReport.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    previous_status = incident.status
    
    incident.status = status

    if status == "verified" and previous_status != "verified":
        new_alert = Alert(
            user_id=incident.user_id,
            alert_type="incident_verified",
            title="Incident Verified",
            message=(
                f"Your reported {incident.incident_type} incident "
                "has been verified by the CityLens administration."
            ),
            severity="warning",
            is_read=0
        )

        db.add(new_alert)

    db.commit()
    db.refresh(incident)

    return incident