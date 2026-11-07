from datetime import date, datetime, timezone

from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReviewCase(Base):

    __tablename__ = "review_cases"

    __table_args__ = (
        CheckConstraint(
            "status IN ('OPEN', 'IN_PROGRESS', "
            "'COMPLETED', 'OVERDUE', 'CANCELLED')",
            name="check_review_status"
        ),
    )

    review_case_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    review_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    review_due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    completed_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer")