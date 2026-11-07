
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document import Document
from app.models.verification import Verification
from app.models.audit_event import AuditEvent
from app.schemas.verification import (
    VerificationCreate,
    VerificationResponse
)

router = APIRouter(
    prefix="/api/verifications",
    tags=["Verifications"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/{document_id}",
    response_model=VerificationResponse,
    status_code=201
)
def verify_document(
    document_id: str,
    verification_data: VerificationCreate,
    db: Session = Depends(get_db)
):
    # 1. Find document
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # 2. Only pending documents can be reviewed
    if document.status != "PENDING":
        raise HTTPException(
            status_code=409,
            detail=f"Document cannot be reviewed. Current status: {document.status}"
        )

    # 3. Rejection requires remarks
    if (
        verification_data.status == "REJECTED"
        and not (verification_data.remarks or "").strip()
    ):
        raise HTTPException(
            status_code=400,
            detail="Remarks are required when rejecting a document"
        )

    now = datetime.now(timezone.utc)

    # 4. Create verification record
    verification = Verification(
        verification_id=f"VER-{uuid4().hex[:16].upper()}",
        document_id=document_id,
        verification_type=verification_data.verification_type,
        status=verification_data.status,
        remarks=verification_data.remarks,
        verified_at=now
    )

    # 5. Update document status
    document.status = verification_data.status

    # 6. Create audit event
    audit_event = AuditEvent(
        audit_event_id=f"AUD-{uuid4().hex[:16].upper()}",
        entity_type="DOCUMENT",
        entity_id=document_id,
        action=f"DOCUMENT_{verification_data.status}",
        performed_by=verification_data.performed_by,
        details=verification_data.remarks
    )

    try:
        db.add(verification)
        db.add(audit_event)
        db.commit()
        db.refresh(verification)

        return verification

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to complete document verification"
        )


# Get verification history for a document
@router.get(
    "/{document_id}",
    response_model=list[VerificationResponse]
)
def get_verification_history(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return (
        db.query(Verification)
        .filter(Verification.document_id == document_id)
        .order_by(Verification.created_at.desc())
        .all()
    )
