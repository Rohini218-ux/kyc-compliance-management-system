
from sqlalchemy import text
from app.database import SessionLocal


ANOMALY_CHECKS = [
    (
        "AN-001: Document verification mismatch",
        """
        SELECT COUNT(*)
        FROM documents d
        JOIN verifications v ON v.document_id = d.document_id
        WHERE d.status = 'VERIFIED'
        AND v.status = 'PENDING'
        """
    ),
    (
        "AN-002: Ownership total exceeds 100%",
        """
        SELECT COUNT(*)
        FROM (
            SELECT customer_id
            FROM beneficial_owners
            GROUP BY customer_id
            HAVING SUM(ownership_percentage) > 100
        ) invalid
        """
    ),
    (
        "AN-003: Overdue review with future date",
        """
        SELECT COUNT(*)
        FROM review_cases
        WHERE status = 'OVERDUE'
        AND review_due_date > CURRENT_DATE
        """
    ),
    (
        "AN-004: Future customer onboarding date",
        """
        SELECT COUNT(*)
        FROM customers
        WHERE onboarding_date > CURRENT_DATE
        """
    ),
    (
        "AN-005: Satisfied requirement without verified document",
        """
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
        """
    ),
]


def verify_anomalies():
    session = SessionLocal()

    try:
        print("\nINJECTED ANOMALY VERIFICATION")
        print("=" * 65)

        detected = 0

        for description, query in ANOMALY_CHECKS:
            count = session.execute(text(query)).scalar()

            if count > 0:
                detected += 1
                print(f"DETECTED | {description} | Records: {count}")
            else:
                print(f"NOT DETECTED | {description}")

        print("=" * 65)
        print(f"Total anomalies: {len(ANOMALY_CHECKS)}")
        print(f"Detected: {detected}")
        print(f"Not detected: {len(ANOMALY_CHECKS) - detected}")

    finally:
        session.close()


if __name__ == "__main__":
    verify_anomalies()
