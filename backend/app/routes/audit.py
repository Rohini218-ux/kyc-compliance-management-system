from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.audit_event import AuditEvent
from app.schemas.audit import AuditEventResponse


router = APIRouter(
    prefix="/api/audit-logs",
    tags=["Audit Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get audit logs with optional filters
@router.get("/", response_model=list[AuditEventResponse])
def get_audit_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    entity_type: str | None = None,
    entity_id: str | None = None,
    performed_by: str | None = None,
    action: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(AuditEvent)

    if entity_type:
        query = query.filter(AuditEvent.entity_type == entity_type)

    if entity_id:
        query = query.filter(AuditEvent.entity_id == entity_id)

    if performed_by:
        query = query.filter(AuditEvent.performed_by == performed_by)

    if action:
        query = query.filter(AuditEvent.action == action)

    return (
        query
        .order_by(AuditEvent.event_timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# Get one audit event
@router.get("/{audit_event_id}", response_model=AuditEventResponse)
def get_audit_event(
    audit_event_id: str,
    db: Session = Depends(get_db)
):
    event = db.get(AuditEvent, audit_event_id)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Audit event not found"
        )

    return event