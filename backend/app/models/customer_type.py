from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Boolean,
    Date,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base




class CustomerType(Base):

    __tablename__ = "customer_types"

    # Primary key
    customer_type_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    # Customer type code
    type_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    # Customer type name
    type_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    # Relationship with Customer (Target string "Customer" added explicitly)
    customers: Mapped[list["Customer"]] = relationship(
        "Customer",
        back_populates="customer_type"
    )
