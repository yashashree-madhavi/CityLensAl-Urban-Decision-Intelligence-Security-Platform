from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertResponse
from app.security.auth import get_current_user

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "",
    response_model=list[AlertResponse]
)
def get_my_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Alert)
        .filter(
            (Alert.user_id == current_user.id)
            | (Alert.user_id.is_(None))
        )
        .order_by(Alert.created_at.desc())
        .all()
    )

@router.get("/unread-count")
def get_unread_alert_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = (
        db.query(Alert)
        .filter(
            Alert.user_id == current_user.id,
            Alert.is_read == 0
        )
        .count()
    )

    return {
        "unread_count": count
    }

@router.patch("/{alert_id}/read")
def mark_alert_as_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.user_id == current_user.id
        )
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.is_read = 1

    db.commit()
    db.refresh(alert)

    return alert


@router.post(
    "",
    response_model=AlertResponse,
    status_code=201
)
def create_alert(
    alert_type: str,
    title: str,
    message: str,
    severity: str = "info",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_alert = Alert(
        user_id=current_user.id,
        alert_type=alert_type,
        title=title,
        message=message,
        severity=severity,
        is_read=0
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert
