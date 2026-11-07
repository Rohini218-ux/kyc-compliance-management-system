from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditEvent(Base):

    __tablename__ = "audit_events"

    audit_event_id: Mapped[str] = mapped_column(
        String(40),
        primary_key=True
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    entity_id: Mapped[str] = mapped_column(
        String(40),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    performed_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )