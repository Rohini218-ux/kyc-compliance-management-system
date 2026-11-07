
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.customer_type import CustomerType
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Generate customer ID
def generate_customer_id(db: Session) -> str:
    while True:
        customer_id = f"CUS-{uuid4().hex[:12].upper()}"

        existing = db.get(Customer, customer_id)

        if existing is None:
            return customer_id


# 1. Create customer
@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    customer_type = db.get(
        CustomerType,
        customer_data.customer_type_id
    )

    if customer_type is None:
        raise HTTPException(
            status_code=404,
            detail="Customer type not found"
        )

    if not customer_type.is_active:
        raise HTTPException(
            status_code=400,
            detail="Customer type is inactive"
        )

    customer = Customer(
        customer_id=generate_customer_id(db),
        **customer_data.model_dump()
    )

    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create customer"
        )


# 2. List customers with pagination
@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return (
        db.query(Customer)
        .order_by(Customer.customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# 3. Get one customer
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# 4. Update customer
@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: str,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    updates = customer_data.model_dump(exclude_unset=True)

    if "customer_type_id" in updates:
        customer_type = db.get(
            CustomerType,
            updates["customer_type_id"]
        )

        if customer_type is None:
            raise HTTPException(
                status_code=404,
                detail="Customer type not found"
            )

        if not customer_type.is_active:
            raise HTTPException(
                status_code=400,
                detail="Customer type is inactive"
            )

    for field, value in updates.items():
        setattr(customer, field, value)

    try:
        db.commit()
        db.refresh(customer)
        return customer
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update customer"
        )
