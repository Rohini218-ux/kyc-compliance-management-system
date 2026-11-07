
import random
from datetime import date

from app.database import SessionLocal
from app.models import Customer, BeneficialOwner

SEED = 20261022
random.seed(SEED)


def main():

    with SessionLocal() as db:
        try:
            if db.query(BeneficialOwner).first():
                raise ValueError(
                    "Beneficial owners already exist."
                )

            businesses = (
                db.query(Customer)
                .filter_by(customer_type_id="CT-BUS")
                .order_by(Customer.customer_id)
                .all()
            )

            if len(businesses) != 2000:
                raise ValueError(
                    f"Expected 2000 businesses, found {len(businesses)}"
                )

            owners = []

            for business in businesses:

                owner_count = random.choice([1, 2])

                if owner_count == 1:
                    percentages = [100.00]
                else:
                    first_percentage = random.randint(40, 70)
                    percentages = [
                        float(first_percentage),
                        float(100 - first_percentage)
                    ]

                for index, percentage in enumerate(
                    percentages, start=1
                ):

                    owners.append(
                        BeneficialOwner(
                            beneficial_owner_id=(
                                f"BO-{business.customer_id}-{index:02d}"
                            ),
                            customer_id=business.customer_id,
                            owner_name=f"Owner {index} - "
                                       f"{business.customer_id}",
                            ownership_percentage=percentage,
                            effective_from=business.onboarding_date,
                            effective_to=None,
                        )
                    )

            db.add_all(owners)
            db.commit()

            print("Beneficial owners generated successfully!")
            print(f"Business customers: {len(businesses)}")
            print(f"Beneficial owner records: {len(owners)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
