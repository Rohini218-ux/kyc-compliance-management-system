
from datetime import date

from app.database import SessionLocal
from app.models import (
    Customer,
    RiskRating,
    RequirementApplicability,
    CustomerRequirement,
)

SEED_DATE = date(2026, 1, 1)


def main():

    with SessionLocal() as db:
        try:
            if db.query(CustomerRequirement).first():
                raise ValueError(
                    "Customer requirements already exist. "
                    "Avoid generating duplicates."
                )

            customers = (
                db.query(Customer)
                .order_by(Customer.customer_id)
                .all()
            )

            risk_ratings = db.query(RiskRating).all()

            # Create customer_id -> risk_level mapping
            risk_map = {
                rating.customer_id: rating.risk_level
                for rating in risk_ratings
            }

            # Load all applicability rules
            rules = db.query(RequirementApplicability).all()

            # Create (customer_type_id, risk_level) -> requirements mapping
            rule_map = {}

            for rule in rules:
                key = (rule.customer_type_id, rule.risk_level)

                rule_map.setdefault(key, []).append(rule)

            customer_requirements = []

            for customer in customers:

                risk_level = risk_map.get(customer.customer_id)

                if risk_level is None:
                    raise ValueError(
                        f"Risk rating missing for {customer.customer_id}"
                    )

                key = (customer.customer_type_id, risk_level)

                applicable_rules = rule_map.get(key, [])

                for rule in applicable_rules:

                    customer_requirements.append(
                        CustomerRequirement(
                            customer_requirement_id=(
                                f"CR-{customer.customer_id}-"
                                f"{rule.requirement_id}"
                            ),
                            customer_id=customer.customer_id,
                            requirement_id=rule.requirement_id,
                            status="PENDING",
                            assigned_date=customer.onboarding_date,
                            completed_date=None,
                        )
                    )

            db.add_all(customer_requirements)
            db.commit()

            print("Customer requirements generated successfully!")
            print(f"Customers processed: {len(customers)}")
            print(
                f"Requirements assigned: "
                f"{len(customer_requirements)}"
            )

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
