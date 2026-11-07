
from sqlalchemy import text
from app.database import SessionLocal


def validate_customer_dates(session):
    print("\nCUSTOMER DATE VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM customers
        WHERE onboarding_date > CURRENT_DATE
    """)

    future_onboarding_dates = session.execute(query).scalar()

    if future_onboarding_dates == 0:
        print("PASS | No future onboarding dates")
    else:
        print(
            f"FAIL | Future onboarding dates: "
            f"{future_onboarding_dates}"
        )

    return future_onboarding_dates == 0


def validate_review_dates(session):
    print("\nREVIEW DATE VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM review_cases
        WHERE completed_date IS NOT NULL
        AND completed_date < created_at::date
    """)

    invalid_dates = session.execute(query).scalar()

    if invalid_dates == 0:
        print("PASS | Review completion dates are valid")
    else:
        print(f"FAIL | Invalid review completion dates: {invalid_dates}")

    return invalid_dates == 0


def validate_ownership_percentage(session):
    print("\nOWNERSHIP PERCENTAGE VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM beneficial_owners
        WHERE ownership_percentage <= 0
        OR ownership_percentage > 100
    """)

    invalid_percentages = session.execute(query).scalar()

    if invalid_percentages == 0:
        print("PASS | Ownership percentages are within 0-100")
    else:
        print(f"FAIL | Invalid ownership percentages: {invalid_percentages}")

    return invalid_percentages == 0


def run_validation():
    session = SessionLocal()

    try:
        results = [
            validate_customer_dates(session),
            validate_review_dates(session),
            validate_ownership_percentage(session),
        ]

        print("\n" + "=" * 60)
        print("DATE AND ARITHMETIC VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total checks: {len(results)}")
        print(f"Passed: {sum(results)}")
        print(f"Failed: {len(results) - sum(results)}")

    finally:
        session.close()


if __name__ == "__main__":
    run_validation()
