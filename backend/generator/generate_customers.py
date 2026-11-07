
import random
from datetime import date, datetime, time, timezone, timedelta

import numpy as np
from faker import Faker

from app.database import SessionLocal
from app.models import Customer, CustomerType

SEED = 20261022
TOTAL_CUSTOMERS = 8000
INDIVIDUAL_COUNT = 6000
BUSINESS_COUNT = 2000

fake = Faker("en_IN")
Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

STATUSES = ["ONBOARDING", "PENDING", "APPROVED", "REJECTED", "SUSPENDED"]
STATUS_WEIGHTS = [10, 20, 50, 10, 10]


def generate_customer(index, customer_type_id):
    onboarding_date = fake.date_between_dates(
        date_start=date(2024, 1, 1),
        date_end=date(2026, 10, 31),
    )

    if customer_type_id == "CT-IND":
        customer_name = fake.name()
        date_of_birth = fake.date_of_birth(
            minimum_age=18,
            maximum_age=80,
        )
    else:
        customer_name = fake.company()
        date_of_birth = None

    status = random.choices(
        STATUSES,
        weights=STATUS_WEIGHTS,
        k=1,
    )[0]

    created_at = datetime.combine(
        onboarding_date,
        time(hour=10),
        tzinfo=timezone.utc,
    )

    return Customer(
        customer_id=f"CUS-{index:06d}",
        customer_type_id=customer_type_id,
        customer_name=customer_name,
        date_of_birth=date_of_birth,
        onboarding_date=onboarding_date,
        status=status,
        created_at=created_at,
    )


def main():
    with SessionLocal() as db:
        try:
            if db.query(Customer).first():
                raise RuntimeError(
                    "Customer records already exist. "
                    "Do not generate duplicates."
                )

            customer_types = {
                item.customer_type_id
                for item in db.query(CustomerType).all()
            }

            if not {"CT-IND", "CT-BUS"}.issubset(customer_types):
                raise RuntimeError("Reference customer types are missing.")

            customers = []

            for index in range(1, INDIVIDUAL_COUNT + 1):
                customers.append(
                    generate_customer(index, "CT-IND")
                )

            for index in range(
                INDIVIDUAL_COUNT + 1,
                TOTAL_CUSTOMERS + 1,
            ):
                customers.append(
                    generate_customer(index, "CT-BUS")
                )

            db.add_all(customers)
            db.commit()

            print(f"Successfully generated {len(customers)} customers.")
            print(f"Individual customers: {INDIVIDUAL_COUNT}")
            print(f"Business customers: {BUSINESS_COUNT}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
