
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.customer_requirement import CustomerRequirement
from app.models.kyc_requirement import KYCRequirement
from app.models.document import Document

from app.schemas.compliance import (
    ComplianceResponse,
    RequirementDetail
)


router = APIRouter(
    prefix="/api/compliance",
    tags=["Compliance"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{customer_id}",
    response_model=ComplianceResponse
)
def get_customer_compliance(
    customer_id: str,
    db: Session = Depends(get_db)
):
    # 1. Check whether the customer exists
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # 2. Fetch all requirements assigned to this customer
    requirements = (
        db.query(CustomerRequirement, KYCRequirement)
        .join(
            KYCRequirement,
            CustomerRequirement.requirement_id
            == KYCRequirement.requirement_id
        )
        .filter(
            CustomerRequirement.customer_id == customer_id
        )
        .all()
    )

    # 3. Initialize counters
    total = 0
    satisfied = 0
    pending = 0
    rejected = 0
    waived = 0

    requirement_details = []

    # 4. Evaluate every customer requirement
    for customer_req, kyc_req in requirements:

        # Fetch documents linked to this requirement
        documents = (
            db.query(Document)
            .filter(
                Document.customer_requirement_id
                == customer_req.customer_requirement_id
            )
            .all()
        )

        # Match document types
        expected_type = (
            kyc_req.document_type or ""
        ).strip().upper()

        matching_documents = [
            doc for doc in documents
            if (
                doc.document_type or ""
            ).strip().upper() == expected_type
        ]

        # 5. Determine document status
        if any(
            doc.status == "VERIFIED"
            for doc in matching_documents
        ):
            document_status = "VERIFIED"

        elif any(
            doc.status == "PENDING"
            for doc in matching_documents
        ):
            document_status = "PENDING"

        elif any(
            doc.status == "REJECTED"
            for doc in matching_documents
        ):
            document_status = "REJECTED"

        else:
            document_status = None

        # 6. Determine effective requirement status
        stored_status = (
            customer_req.status or ""
        ).strip().upper()

        if stored_status == "WAIVED":
            effective_status = "WAIVED"

        elif stored_status == "REJECTED":
            effective_status = "REJECTED"

        elif document_status == "VERIFIED":
            effective_status = "SATISFIED"

        elif document_status == "REJECTED":
            effective_status = "REJECTED"

        else:
            effective_status = "PENDING"

        # 7. Update summary counters
        if effective_status == "WAIVED":
            waived += 1

        else:
            total += 1

            if effective_status == "SATISFIED":
                satisfied += 1

            elif effective_status == "REJECTED":
                rejected += 1

            else:
                pending += 1

        # 8. Add requirement details
        requirement_details.append(
            RequirementDetail(
                customer_requirement_id=(
                    customer_req.customer_requirement_id
                ),
                requirement_id=kyc_req.requirement_id,
                requirement_name=kyc_req.requirement_name,
                document_type=kyc_req.document_type,
                requirement_status=effective_status,
                document_status=document_status
            )
        )

    # 9. Calculate completion percentage
    percentage = (
        round((satisfied / total) * 100, 2)
        if total > 0
        else 0.0
    )

    # 10. Determine overall compliance status
    if total == 0:
        compliance_status = "NO_REQUIREMENTS"

    elif rejected > 0:
        compliance_status = "ACTION_REQUIRED"

    elif satisfied == total:
        compliance_status = "COMPLETE"

    else:
        compliance_status = "INCOMPLETE"

    # 11. Return compliance response
    return ComplianceResponse(
        customer_id=customer_id,
        total_requirements=total,
        satisfied_requirements=satisfied,
        pending_requirements=pending,
        rejected_requirements=rejected,
        waived_requirements=waived,
        completion_percentage=percentage,
        compliance_status=compliance_status,
        requirements=requirement_details
    )
