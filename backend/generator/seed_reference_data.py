
from datetime import date

from app.database import SessionLocal
from app.models import (
    CustomerType,
    KYCRequirement,
    RequirementApplicability,
)

SEED_DATE = date(2026, 1, 1)

CUSTOMER_TYPES = [
    {
        "customer_type_id": "CT-IND",
        "type_code": "IND",
        "type_name": "Individual",
        "description": "Individual customer",
    },
    {
        "customer_type_id": "CT-BUS",
        "type_code": "BUS",
        "type_name": "Business",
        "description": "Business customer",
    },
]

REQUIREMENTS = [
    {
        "requirement_id": "KYC-2026-000001",
        "requirement_code": "IDENTITY_PROOF",
        "requirement_name": "Identity Proof",
        "document_type": "IDENTITY",
    },
    {
        "requirement_id": "KYC-2026-000002",
        "requirement_code": "ADDRESS_PROOF",
        "requirement_name": "Address Proof",
        "document_type": "ADDRESS",
    },
    {
        "requirement_id": "KYC-2026-000003",
        "requirement_code": "TAX_IDENTIFICATION",
        "requirement_name": "Tax Identification",
        "document_type": "TAX",
    },
    {
        "requirement_id": "KYC-2026-000004",
        "requirement_code": "BUSINESS_REGISTRATION",
        "requirement_name": "Business Registration",
        "document_type": "BUSINESS_REGISTRATION",
    },
    {
        "requirement_id": "KYC-2026-000005",
        "requirement_code": "BENEFICIAL_OWNERSHIP",
        "requirement_name": "Beneficial Ownership",
        "document_type": "OWNERSHIP",
    },
]

APPLICABILITY = {
    "CT-IND": [
        "KYC-2026-000001",
        "KYC-2026-000002",
        "KYC-2026-000003",
    ],
    "CT-BUS": [
        "KYC-2026-000003",
        "KYC-2026-000004",
        "KYC-2026-000005",
    ],
}


def seed_customer_types(db):
    for item in CUSTOMER_TYPES:
        exists = db.query(CustomerType).filter_by(
            customer_type_id=item["customer_type_id"]
        ).first()

        if not exists:
            db.add(
                CustomerType(
                    **item,
                    is_active=True,
                    effective_from=SEED_DATE,
                )
            )


def seed_requirements(db):
    for item in REQUIREMENTS:
        exists = db.query(KYCRequirement).filter_by(
            requirement_id=item["requirement_id"]
        ).first()

        if not exists:
            db.add(
                KYCRequirement(
                    **item,
                    description=f"Synthetic requirement: {item['requirement_name']}",
                    is_mandatory=True,
                    is_active=True,
                    effective_from=SEED_DATE,
                )
            )


def seed_applicability(db):
    for customer_type_id, requirement_ids in APPLICABILITY.items():
        for requirement_id in requirement_ids:
            for risk_level in ("LOW", "MEDIUM", "HIGH"):
                exists = db.query(RequirementApplicability).filter_by(
                    customer_type_id=customer_type_id,
                    requirement_id=requirement_id,
                    risk_level=risk_level,
                    effective_from=SEED_DATE,
                ).first()

                if not exists:
                    db.add(
                        RequirementApplicability(
                            customer_type_id=customer_type_id,
                            requirement_id=requirement_id,
                            risk_level=risk_level,
                            is_mandatory=True,
                            effective_from=SEED_DATE,
                        )
                    )


def main():
    with SessionLocal() as db:
        try:
            seed_customer_types(db)
            seed_requirements(db)
            seed_applicability(db)

            db.commit()
            print("Reference data seeded successfully.")

        except Exception:
            db.rollback()
            raise

    print("Customer types: 2")
    print("KYC requirements: 5")
    print("Applicability records: 18")


if __name__ == "__main__":
    main()
