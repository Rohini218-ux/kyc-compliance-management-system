
from sqlalchemy import text
from app.database import SessionLocal


def validate_review_cases(session):
    print("\nREVIEW CASE VALIDATION")
    print("-" * 60)

    checks = [
        (
            "Completed reviews must have completion dates",
            """
            SELECT COUNT(*)
            FROM review_cases
            WHERE status = 'COMPLETED'
            AND completed_date IS NULL
            """
        ),
        (
            "Incomplete reviews must not have completion dates",
            """
            SELECT COUNT(*)
            FROM review_cases
            WHERE status IN ('OPEN', 'IN_PROGRESS', 'OVERDUE')
            AND completed_date IS NOT NULL
            """
        ),
        (
            "Overdue reviews must have past due dates",
            """
            SELECT COUNT(*)
            FROM review_cases
            WHERE status = 'OVERDUE'
            AND review_due_date >= CURRENT_DATE
            """
        ),
    ]

    failed = 0

    for description, query in checks:
        count = session.execute(text(query)).scalar()

        if count == 0:
            print(f"PASS | {description}")
        else:
            failed += 1
            print(f"FAIL | {description} | Records: {count}")

    return len(checks), failed


def validate_beneficial_ownership(session):
    print("\nBENEFICIAL OWNERSHIP VALIDATION")
    print("-" * 60)

    query = text("""
        SELECT COUNT(*)
        FROM (
            SELECT c.customer_id
            FROM customers c
            JOIN beneficial_owners bo
                ON bo.customer_id = c.customer_id
            GROUP BY c.customer_id
            HAVING ABS(SUM(bo.ownership_percentage) - 100) > 0.01
        ) AS invalid_ownership
    """)

    invalid_count = session.execute(query).scalar()

    if invalid_count == 0:
        print("PASS | Beneficial ownership totals equal 100%")
    else:
        print(
            f"FAIL | Customers with invalid ownership totals: "
            f"{invalid_count}"
        )

    return 1, int(invalid_count > 0)


def run_validation():
    session = SessionLocal()

    try:
        review_total, review_failed = validate_review_cases(session)
        ownership_total, ownership_failed = validate_beneficial_ownership(
            session
        )

        total = review_total + ownership_total
        failed = review_failed + ownership_failed

        print("\n" + "=" * 60)
        print("REVIEW AND OWNERSHIP VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total checks: {total}")
        print(f"Passed: {total - failed}")
        print(f"Failed: {failed}")

    finally:
        session.close()


if __name__ == "__main__":
    run_validation()
