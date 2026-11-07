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


class RiskRating(Base):

    __tablename__ = "risk_ratings"

    __table_args__ = (
        CheckConstraint(
            "risk_level IN ('LOW', 'MEDIUM', 'HIGH')",
            name="check_risk_level"
        ),
    )

    risk_rating_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    customer_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    risk_level: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer")