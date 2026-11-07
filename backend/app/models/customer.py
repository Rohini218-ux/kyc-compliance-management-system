from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base




class Customer(Base):

    __tablename__ = "customers"

    __table_args__ = (
        CheckConstraint(
            "status IN ('ONBOARDING', 'PENDING', "
            "'APPROVED', 'REJECTED', 'SUSPENDED')",
            name="check_customer_status"
        ),
    )

    # Primary key
    customer_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True
    )

    # Foreign key
    customer_type_id: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("customer_types.customer_type_id"),
        nullable=False
    )

    customer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    onboarding_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ONBOARDING",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship with CustomerType (Quotes around "CustomerType" are mandatory here)
    customer_type: Mapped["CustomerType"] = relationship(
        "CustomerType",
        back_populates="customers"
    )
