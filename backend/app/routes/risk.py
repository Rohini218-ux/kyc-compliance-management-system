
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.risk_rating import RiskRating
from app.schemas.risk import (
    RiskResponse,
    CustomerRiskResponse
)

router = APIRouter(
    prefix="/api/risks-management",
    tags=["Risk Management"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_risk(db: Session, customer_id: str):
    today = date.today()

    return (
        db.query(RiskRating)
        .filter(
            RiskRating.customer_id == customer_id,
            RiskRating.effective_from <= today,
            (
                (RiskRating.effective_to.is_(None))
                | (RiskRating.effective_to >= today)
            )
        )
        .order_by(RiskRating.effective_from.desc())
        .first()
    )


# 1. List all current risk ratings
@router.get("/", response_model=list[RiskResponse])
def get_all_risks(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid pagination parameters"
        )

    today = date.today()

    return (
        db.query(RiskRating)
        .filter(
            RiskRating.effective_from <= today,
            (
                (RiskRating.effective_to.is_(None))
                | (RiskRating.effective_to >= today)
            )
        )
        .order_by(RiskRating.customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# 2. List high-risk customers
# IMPORTANT: Keep this BEFORE /{customer_id}
@router.get(
    "/high-risk",
    response_model=list[CustomerRiskResponse]
)
def get_high_risk_customers(
    db: Session = Depends(get_db)
):
    today = date.today()

    records = (
        db.query(Customer, RiskRating)
        .join(
            RiskRating,
            Customer.customer_id == RiskRating.customer_id
        )
        .filter(
            RiskRating.risk_level == "HIGH",
            RiskRating.effective_from <= today,
            (
                (RiskRating.effective_to.is_(None))
                | (RiskRating.effective_to >= today)
            )
        )
        .order_by(Customer.customer_id)
        .all()
    )

    return [
        CustomerRiskResponse(
            customer_id=customer.customer_id,
            customer_name=customer.customer_name,
            customer_status=customer.status,
            risk_level=risk.risk_level,
            reason=risk.reason,
            effective_from=risk.effective_from,
            effective_to=risk.effective_to
        )
        for customer, risk in records
    ]


# 3. Get one customer's current risk
@router.get(
    "/{customer_id}",
    response_model=CustomerRiskResponse
)
def get_customer_risk(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    risk = get_current_risk(db, customer_id)

    if risk is None:
        raise HTTPException(
            status_code=404,
            detail="Current risk rating not found"
        )

    return CustomerRiskResponse(
        customer_id=customer.customer_id,
        customer_name=customer.customer_name,
        customer_status=customer.status,
        risk_level=risk.risk_level,
        reason=risk.reason,
        effective_from=risk.effective_from,
        effective_to=risk.effective_to
    )
