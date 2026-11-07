
from sqlalchemy import text
from app.database import SessionLocal


def validate_document_verifications(session):
    print("\nDOCUMENT AND VERIFICATION CONSISTENCY")
    print("-" * 60)

    checks = [
        (
            "Verified documents must have a verified verification",
            """
            SELECT COUNT(*)
            FROM documents d
            WHERE d.status = 'VERIFIED'
            AND NOT EXISTS (
                SELECT 1
                FROM verifications v
                WHERE v.document_id = d.document_id
                AND v.status = 'VERIFIED'
            )
            """,
        ),
        (
            "Rejected documents must have a rejected verification",
            """
            SELECT COUNT(*)
            FROM documents d
            WHERE d.status = 'REJECTED'
            AND NOT EXISTS (
                SELECT 1
                FROM verifications v
                WHERE v.document_id = d.document_id
                AND v.status = 'REJECTED'
            )
            """,
        ),
        (
            "Pending documents must have a pending verification",
            """
            SELECT COUNT(*)
            FROM documents d
            WHERE d.status = 'PENDING'
            AND NOT EXISTS (
                SELECT 1
                FROM verifications v
                WHERE v.document_id = d.document_id
                AND v.status = 'PENDING'
            )
            """,
        ),
        (
            "Expired documents must not have a verified verification",
            """
            SELECT COUNT(*)
            FROM documents d
            WHERE d.status = 'EXPIRED'
            AND EXISTS (
                SELECT 1
                FROM verifications v
                WHERE v.document_id = d.document_id
                AND v.status = 'VERIFIED'
            )
            """,
        ),
    ]

    failed = 0

    for description, sql in checks:
        invalid_count = session.execute(text(sql)).scalar()

        if invalid_count == 0:
            print(f"PASS | {description}")
        else:
            failed += 1
            print(
                f"FAIL | {description} "
                f"| Invalid records: {invalid_count}"
            )

    print("-" * 60)
    print(f"Total checks: {len(checks)}")
    print(f"Passed: {len(checks) - failed}")
    print(f"Failed: {failed}")

    return failed == 0


def run_validation():
    session = SessionLocal()

    try:
        validate_document_verifications(session)
    finally:
        session.close()


if __name__ == "__main__":
    run_validation()
