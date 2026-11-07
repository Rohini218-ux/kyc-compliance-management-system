
from sqlalchemy import text

from app.database import SessionLocal


# Columns that must not contain NULL values
REQUIRED_COLUMNS = {
    "customers": [
    "customer_id",
    "customer_type_id",
    "customer_name",
    "status",
    "onboarding_date",
    "created_at",
],
    "customer_types": [
        "customer_type_id",
        "type_name",
    ],
    "kyc_requirements": [
        "requirement_id",
        "requirement_name",
    ],
    "customer_requirements": [
        "customer_requirement_id",
        "customer_id",
        "requirement_id",
        "status",
    ],
    "documents": [
        "document_id",
        "customer_id",
        "customer_requirement_id",
        "document_type",
        "status",
    ],
    "verifications": [
        "verification_id",
        "document_id",
        "status",
    ],
    "risk_ratings": [
        "risk_rating_id",
        "customer_id",
        "risk_level",
    ],
    "review_cases": [
    "review_case_id",
    "customer_id",
    "review_type",
    "review_due_date",
    "status",
    "created_at",
],
    "beneficial_owners": [
        "beneficial_owner_id",
        "customer_id",
        "ownership_percentage",
    ],
    "alerts": [
        "alert_id",
        "customer_id",
        "severity",
        "status",
    ],
    "audit_events": [
    "audit_event_id",
    "entity_type",
    "entity_id",
    "action",
    "event_timestamp",
],
    "requirement_applicability": [
        "applicability_id",
        "customer_type_id",
        "requirement_id",
        "risk_level",
    ],
}


def validate_null_values():
    session = SessionLocal()

    try:
        print("\nNULL VALUE VALIDATION")
        print("-" * 60)

        total_checks = 0
        failed_checks = 0

        for table, columns in REQUIRED_COLUMNS.items():
            for column in columns:
                query = text(
                    f"""
                    SELECT COUNT(*)
                    FROM {table}
                    WHERE {column} IS NULL
                    """
                )

                null_count = session.execute(query).scalar()

                total_checks += 1

                if null_count == 0:
                    print(f"PASS | {table}.{column}")
                else:
                    failed_checks += 1
                    print(
                        f"FAIL | {table}.{column} "
                        f"| Missing values: {null_count}"
                    )

        print("-" * 60)
        print(f"Total checks: {total_checks}")
        print(f"Passed: {total_checks - failed_checks}")
        print(f"Failed: {failed_checks}")

        return failed_checks == 0

    finally:
        session.close()


if __name__ == "__main__":
    validate_null_values()
