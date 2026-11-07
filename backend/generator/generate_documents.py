
import random
from datetime import date, datetime, time, timezone, timedelta

from app.database import SessionLocal
from app.models import (
    Customer,
    CustomerRequirement,
    Document,
)

SEED = 20261022
TOTAL_DOCUMENTS = 20000

random.seed(SEED)

DOCUMENT_STATUSES = [
    "PENDING",
    "VERIFIED",
    "REJECTED",
    "EXPIRED",
]

STATUS_WEIGHTS = [20, 55, 10, 15]


def generate_document(index, customer, requirement):

    issue_date = customer.onboarding_date - timedelta(
        days=random.randint(0, 30)
    )

    document_type = requirement.requirement.document_type

    # Illustrative validity periods for synthetic data.
    if document_type == "IDENTITY":
        validity_days = 3650
    elif document_type == "ADDRESS":
        validity_days = 730
    else:
        validity_days = 3650

    expiry_date = issue_date + timedelta(days=validity_days)

    status = random.choices(
        DOCUMENT_STATUSES,
        weights=STATUS_WEIGHTS,
        k=1,
    )[0]

    # Ensure expiry status agrees with expiry date.
    if expiry_date < date(2026, 1, 1):
        status = "EXPIRED"

    uploaded_at = datetime.combine(
        customer.onboarding_date,
        time(hour=10),
        tzinfo=timezone.utc,
    )

    return Document(
        document_id=f"DOC-{index:06d}",
        customer_id=customer.customer_id,
        customer_requirement_id=(
            requirement.customer_requirement_id
        ),
        document_type=document_type,
        document_name=f"{document_type}_{index:06d}.pdf",
        issue_date=issue_date,
        expiry_date=expiry_date,
        status=status,
        uploaded_at=uploaded_at,
    )


def main():

    with SessionLocal() as db:

        try:
            if db.query(Document).first():
                raise ValueError(
                    "Documents already exist. Avoid duplicate generation."
                )

            customers = db.query(Customer).all()

            requirements = (
                db.query(CustomerRequirement)
                .all()
            )

            customer_map = {
                customer.customer_id: customer
                for customer in customers
            }

            if not customers or not requirements:
                raise ValueError(
                    "Customers or customer requirements are missing."
                )

            # Group requirements by customer.
            requirement_map = {}

            for requirement in requirements:
                requirement_map.setdefault(
                    requirement.customer_id, []
                ).append(requirement)

            eligible_pairs = []

            for customer_id, customer_requirements in requirement_map.items():

                customer = customer_map[customer_id]

                for requirement in customer_requirements:
                    eligible_pairs.append((customer, requirement))

            if not eligible_pairs:
                raise ValueError("No eligible customer requirements found.")

            # Allocate documents across eligible requirements.
            selected_pairs = random.choices(
                eligible_pairs,
                k=TOTAL_DOCUMENTS,
            )

            documents = []

            for index, (customer, requirement) in enumerate(
                selected_pairs,
                start=1,
            ):
                documents.append(
                    generate_document(index, customer, requirement)
                )

            db.add_all(documents)
            db.commit()

            print("Document generation successful!")
            print(f"Total documents: {len(documents)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
