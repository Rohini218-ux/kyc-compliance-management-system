
import random
from datetime import date, datetime, time, timezone

from app.database import SessionLocal
from app.models import Customer, ReviewCase

SEED = 20261022
TOTAL_REVIEWS = 3000

random.seed(SEED)

REVIEW_STATUSES = [
    "OPEN",
    "IN_PROGRESS",
    "COMPLETED",
    "OVERDUE",
    "CANCELLED",
]

STATUS_WEIGHTS = [25, 20, 35, 15, 5]


def main():

    with SessionLocal() as db:
        try:
            if db.query(ReviewCase).first():
                raise ValueError("Review cases already exist.")

            customers = (
                db.query(Customer)
                .order_by(Customer.customer_id)
                .all()
            )

            if len(customers) != 8000:
                raise ValueError(
                    f"Expected 8000 customers, found {len(customers)}"
                )

            selected_customers = random.sample(
                customers,
                TOTAL_REVIEWS,
            )

            reviews = []

            for index, customer in enumerate(
                selected_customers,
                start=1,
            ):

                due_date = date(2026, 10, 1)

                status = random.choices(
                    REVIEW_STATUSES,
                    weights=STATUS_WEIGHTS,
                    k=1,
                )[0]

                completed_date = None

                if status == "COMPLETED":
                    completed_date = date(2026, 9, 15)

                reviews.append(
                    ReviewCase(
                        review_case_id=(
                            f"REV-{customer.customer_id}-2026"
                        ),
                        customer_id=customer.customer_id,
                        review_type="PERIODIC",
                        review_due_date=due_date,
                        completed_date=completed_date,
                        status=status,
                        remarks=f"Synthetic periodic review {index}",
                        created_at=datetime.combine(
                            customer.onboarding_date,
                            time(hour=10),
                            tzinfo=timezone.utc,
                        ),
                    )
                )

            db.add_all(reviews)
            db.commit()

            print("Review case generation successful!")
            print(f"Total review cases: {len(reviews)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
