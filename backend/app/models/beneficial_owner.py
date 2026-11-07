from datetime import date

from sqlalchemy import (
    String,
    Date,
    Numeric,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BeneficialOwner(Base):

    __tablename__ = "beneficial_owners"

    __table_args__ = (
        CheckConstraint(
            "ownership_percentage > 0 "
            "AND ownership_percentage <= 100",
            name="check_ownership_percentage"
        ),
    )

    beneficial_owner_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    owner_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    ownership_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    customer: Mapped["Customer"] = relationship("Customer")