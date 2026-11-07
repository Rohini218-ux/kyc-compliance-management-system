from datetime import date, datetime, timezone

from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'VERIFIED', 'REJECTED', 'EXPIRED')",
            name="check_document_status"
        ),
    )

    document_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    document_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    issue_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    customer_requirement_id: Mapped[str] = mapped_column(
    String(40),
    ForeignKey(
        "customer_requirements.customer_requirement_id"
    ),
    nullable=False
   )

    customer: Mapped["Customer"] = relationship("Customer")