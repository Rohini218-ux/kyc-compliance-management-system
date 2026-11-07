
from sqlalchemy import text
from app.database import SessionLocal


def validate_kyc_completeness(session):
    print("\nKYC COMPLETENESS VALIDATION")
    print("-" * 60)

    # Check 1: Every customer must have at least one KYC requirement.
    query_1 = text("""
        SELECT COUNT(*)
        FROM customers c
        WHERE NOT EXISTS (
            SELECT 1
            FROM customer_requirements cr
            WHERE cr.customer_id = c.customer_id
        )
    """)

    customers_without_requirements = session.execute(query_1).scalar()

    # Check 2: Every satisfied requirement must have a verified document.
    query_2 = text("""
        SELECT COUNT(*)
        FROM customer_requirements cr
        WHERE cr.status = 'SATISFIED'
        AND NOT EXISTS (
            SELECT 1
            FROM documents d
            JOIN verifications v
                ON v.document_id = d.document_id
            WHERE d.customer_requirement_id =
                  cr.customer_requirement_id
            AND d.status = 'VERIFIED'
            AND v.status = 'VERIFIED'
        )
    """)

    satisfied_without_verified_docs = session.execute(query_2).scalar()

    # Check 3: A requirement cannot be both WAIVED and have no reason.
    # This is only a preliminary check; the actual waiver reason
    # column must be confirmed in the database schema.
    print(
        f"Customers without requirements: "
        f"{customers_without_requirements}"
    )

    print(
        f"Satisfied requirements without verified documents: "
        f"{satisfied_without_verified_docs}"
    )

    print("-" * 60)

    checks = [
        customers_without_requirements,
        satisfied_without_verified_docs,
    ]

    print(f"Total checks: {len(checks)}")
    print(f"Passed: {sum(count == 0 for count in checks)}")
    print(f"Failed: {sum(count > 0 for count in checks)}")

    return all(count == 0 for count in checks)


def run_validation():
    session = SessionLocal()

    try:
        validate_kyc_completeness(session)
    finally:
        session.close()


if __name__ == "__main__":
    run_validation()
