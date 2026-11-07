
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.alert import Alert
from app.models.audit_event import AuditEvent
from app.schemas.alert import AlertUpdate, AlertResponse

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alert Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. List all alerts
@router.get("/", response_model=list[AlertResponse])
def get_alerts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid pagination parameters"
        )

    return (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# 2. List unresolved alerts
# Keep this route before /{alert_id}
@router.get("/open", response_model=list[AlertResponse])
def get_open_alerts(
    db: Session = Depends(get_db)
):
    return (
        db.query(Alert)
        .filter(Alert.status.in_(["OPEN", "ACKNOWLEDGED"]))
        .order_by(Alert.created_at.desc())
        .all()
    )


# 3. Get one alert
@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


# 4. Update alert status
@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: str,
    update_data: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = db.get(Alert, alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    if alert.status == "RESOLVED":
        raise HTTPException(
            status_code=409,
            detail="Resolved alerts cannot be updated"
        )

    old_status = alert.status
    new_status = update_data.status

    alert.status = new_status

    if new_status == "RESOLVED":
        alert.resolved_at = datetime.now(timezone.utc)

    details = (
        f"Status changed from {old_status} to {new_status}."
    )

    if update_data.remarks:
        details += f" Remarks: {update_data.remarks}"

    audit_event = AuditEvent(
        audit_event_id=f"AUD-{uuid4().hex[:16].upper()}",
        entity_type="ALERT",
        entity_id=alert_id,
        action="ALERT_STATUS_UPDATED",
        performed_by=update_data.performed_by,
        details=details
    )

    try:
        db.add(audit_event)
        db.commit()
        db.refresh(alert)
        return alert

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update alert"
        )
