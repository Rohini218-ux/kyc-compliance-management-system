from datetime import date

from sqlalchemy import (
    String,
    Boolean,
    Date,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base



class KYCRequirement(Base):

    __tablename__ = "kyc_requirements"

    # Primary key
    requirement_id: Mapped[str] = mapped_column(
        String(30),
        primary_key=True
    )

    requirement_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    requirement_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_mandatory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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

    # Relationship with applicability
    applicability: Mapped[list["RequirementApplicability"]] = relationship(
        back_populates="requirement"
    )