
import random
from datetime import date, datetime, time, timezone

from app.database import SessionLocal
from app.models import Customer, RiskRating

SEED = 20261022

random.seed(SEED)

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH"]
RISK_WEIGHTS = [50, 35, 15]

RISK_REASONS = {
    "LOW": "Standard customer risk profile",
    "MEDIUM": "Moderate customer risk indicators",
    "HIGH": "Elevated customer risk indicators",
}


def main():

    with SessionLocal() as db:

        try:
            customers = (
                db.query(Customer)
                .order_by(Customer.customer_id)
                .all()
            )

            if len(customers) != 8000:
                raise ValueError(
                    f"Expected 8000 customers, found {len(customers)}"
                )

            if db.query(RiskRating).first():
                raise ValueError(
                    "Risk ratings already exist. "
                    "Avoid generating duplicates."
                )

            risk_ratings = []

            for index, customer in enumerate(customers, start=1):

                risk_level = random.choices(
                    RISK_LEVELS,
                    weights=RISK_WEIGHTS,
                    k=1
                )[0]

                risk_rating = RiskRating(
                    risk_rating_id=f"RSK-{index:06d}",
                    customer_id=customer.customer_id,
                    risk_level=risk_level,
                    reason=RISK_REASONS[risk_level],
                    effective_from=customer.onboarding_date,
                    effective_to=None,
                    created_at=datetime.combine(
                        customer.onboarding_date,
                        time(hour=10),
                        tzinfo=timezone.utc
                    )
                )

                risk_ratings.append(risk_rating)

            db.add_all(risk_ratings)
            db.commit()

            print("Risk ratings generated successfully!")
            print(f"Total risk ratings: {len(risk_ratings)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
