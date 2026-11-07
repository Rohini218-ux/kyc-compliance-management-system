from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Verification(Base):

    __tablename__ = "verifications"

    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'VERIFIED', 'REJECTED')",
            name="check_verification_status"
        ),
    )

    verification_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    document_id: Mapped[str] = mapped_column(
        String(40),
        ForeignKey("documents.document_id"),
        nullable=False
    )

    verification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    document: Mapped["Document"] = relationship("Document")