from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.document import Document
from app.models.risk_rating import RiskRating
from app.models.alert import Alert
from app.models.review_case import ReviewCase
from app.schemas.dashboard import DashboardResponse


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary", response_model=DashboardResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):

    today = date.today()

    return DashboardResponse(
        total_customers=db.query(Customer).count(),

        approved_customers=db.query(Customer).filter(
            Customer.status == "APPROVED"
        ).count(),

        pending_customers=db.query(Customer).filter(
            Customer.status == "PENDING"
        ).count(),

        total_documents=db.query(Document).count(),

        pending_documents=db.query(Document).filter(
            Document.status == "PENDING"
        ).count(),

        verified_documents=db.query(Document).filter(
            Document.status == "VERIFIED"
        ).count(),

        rejected_documents=db.query(Document).filter(
            Document.status == "REJECTED"
        ).count(),

        high_risk_customers=db.query(RiskRating).filter(
            RiskRating.risk_level == "HIGH",
            RiskRating.effective_from <= today,
            (RiskRating.effective_to.is_(None)) |
            (RiskRating.effective_to >= today)
        ).count(),

        open_alerts=db.query(Alert).filter(
            Alert.status.in_(["OPEN", "ACKNOWLEDGED"])
        ).count(),

        overdue_reviews=db.query(ReviewCase).filter(
            ReviewCase.review_due_date < today,
            ReviewCase.status.in_(["OPEN", "IN_PROGRESS", "OVERDUE"])
        ).count()
    )