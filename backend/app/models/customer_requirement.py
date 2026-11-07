from datetime import date

from sqlalchemy import (
    String,
    Date,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CustomerRequirement(Base):

    __tablename__ = "customer_requirements"

    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'SATISFIED', 'WAIVED', 'REJECTED')",
            name="check_customer_requirement_status"
        ),
        UniqueConstraint(
            "customer_id",
            "requirement_id",
            name="uq_customer_requirement"
        ),
    )

    customer_requirement_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    requirement_id: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("kyc_requirements.requirement_id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    assigned_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    completed_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    customer: Mapped["Customer"] = relationship("Customer")

    requirement: Mapped["KYCRequirement"] = relationship(
        "KYCRequirement"
    )