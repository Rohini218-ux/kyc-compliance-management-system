from datetime import date

from sqlalchemy import (
    String,
    Date,
    Boolean,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Integer
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class RequirementApplicability(Base):

    __tablename__ = "requirement_applicability"

    __table_args__ = (

        CheckConstraint(
            "risk_level IN ('LOW', 'MEDIUM', 'HIGH')",
            name="check_applicability_risk_level"
        ),

        UniqueConstraint(
            "customer_type_id",
            "requirement_id",
            "risk_level",
            "effective_from",
            name="uq_requirement_applicability"
        ),

    )

    # Primary key
    applicability_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Foreign key: CustomerType
    customer_type_id: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("customer_types.customer_type_id"),
        nullable=False
    )

    # Foreign key: KYCRequirement
    requirement_id: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("kyc_requirements.requirement_id"),
        nullable=False
    )

    risk_level: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    is_mandatory: Mapped[bool] = mapped_column(
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

    # Relationships
    customer_type: Mapped["CustomerType"] = relationship()

    requirement: Mapped["KYCRequirement"] = relationship(
        back_populates="applicability"
    )