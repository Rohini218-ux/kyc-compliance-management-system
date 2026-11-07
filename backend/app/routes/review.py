
from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.review_case import ReviewCase
from app.models.audit_event import AuditEvent
from app.schemas.review import ReviewUpdate, ReviewResponse


router = APIRouter(
    prefix="/api/reviews",
    tags=["Review Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. List reviews
@router.get("/", response_model=list[ReviewResponse])
def get_reviews(
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
        db.query(ReviewCase)
        .order_by(ReviewCase.review_due_date)
        .offset(skip)
        .limit(limit)
        .all()
    )


# 2. Get overdue reviews
# IMPORTANT: Must be above /{review_case_id}
@router.get("/overdue", response_model=list[ReviewResponse])
def get_overdue_reviews(
    db: Session = Depends(get_db)
):
    today = date.today()

    return (
        db.query(ReviewCase)
        .filter(
            ReviewCase.review_due_date < today,
            ReviewCase.status.in_([
                "OPEN",
                "IN_PROGRESS",
                "OVERDUE"
            ])
        )
        .order_by(ReviewCase.review_due_date)
        .all()
    )


# 3. Get one review
@router.get(
    "/{review_case_id}",
    response_model=ReviewResponse
)
def get_review(
    review_case_id: str,
    db: Session = Depends(get_db)
):
    review = db.get(ReviewCase, review_case_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review case not found"
        )

    return review


# 4. Update review
@router.patch(
    "/{review_case_id}",
    response_model=ReviewResponse
)
def update_review(
    review_case_id: str,
    update_data: ReviewUpdate,
    db: Session = Depends(get_db)
):
    review = db.get(ReviewCase, review_case_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review case not found"
        )

    if review.status in ("COMPLETED", "CANCELLED"):
        raise HTTPException(
            status_code=409,
            detail="Completed or cancelled reviews cannot be updated"
        )

    if update_data.status == "OVERDUE":
        if review.review_due_date >= date.today():
            raise HTTPException(
                status_code=400,
                detail="Review cannot be marked overdue before its due date"
            )

    if update_data.status == "COMPLETED":
        review.completed_date = date.today()
    else:
        review.completed_date = None

    old_status = review.status

    review.status = update_data.status
    review.remarks = update_data.remarks

    audit_event = AuditEvent(
        audit_event_id=f"AUD-{uuid4().hex[:16].upper()}",
        entity_type="REVIEW_CASE",
        entity_id=review_case_id,
        action="REVIEW_STATUS_UPDATED",
        performed_by="api_user",
        details=(
            f"Status changed from {old_status} "
            f"to {update_data.status}"
        )
    )

    try:
        db.add(audit_event)
        db.commit()
        db.refresh(review)
        return review

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update review"
        )
