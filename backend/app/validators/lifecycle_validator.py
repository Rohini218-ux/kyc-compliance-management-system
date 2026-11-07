
from sqlalchemy import text
from app.database import SessionLocal


STATUS_RULES = {
    "customers": {
        "column": "status",
        "allowed": [
            "ONBOARDING",
            "PENDING",
            "APPROVED",
            "REJECTED",
            "SUSPENDED",
        ],
    },
    "customer_requirements": {
        "column": "status",
        "allowed": [
            "PENDING",
            "SATISFIED",
            "WAIVED",
            "REJECTED",
        ],
    },
    "documents": {
        "column": "status",
        "allowed": [
            "PENDING",
            "VERIFIED",
            "REJECTED",
            "EXPIRED",
        ],
    },
    "verifications": {
        "column": "status",
        "allowed": [
            "PENDING",
            "VERIFIED",
            "REJECTED",
        ],
    },
    "review_cases": {
        "column": "status",
        "allowed": [
            "OPEN",
            "IN_PROGRESS",
            "COMPLETED",
            "OVERDUE",
            "CANCELLED",
        ],
    },
    "alerts": {
        "column": "status",
        "allowed": [
            "OPEN",
            "ACKNOWLEDGED",
            "RESOLVED",
        ],
    },
}


def validate_lifecycle_statuses(session):
    print("\nLIFECYCLE STATUS VALIDATION")
    print("-" * 60)

    total_checks = 0
    failed_checks = 0

    for table, rule in STATUS_RULES.items():
        column = rule["column"]
        allowed = rule["allowed"]

        placeholders = ", ".join(
            f":status_{i}" for i in range(len(allowed))
        )

        query = text(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE {column} NOT IN ({placeholders})
               OR {column} IS NULL
        """)

        params = {
            f"status_{i}": status
            for i, status in enumerate(allowed)
        }

        invalid_count = session.execute(query, params).scalar()

        total_checks += 1

        if invalid_count == 0:
            print(f"PASS | {table}.{column}")
        else:
            failed_checks += 1
            print(
                f"FAIL | {table}.{column} "
                f"| Invalid records: {invalid_count}"
            )

    print("-" * 60)
    print(f"Total checks: {total_checks}")
    print(f"Passed: {total_checks - failed_checks}")
    print(f"Failed: {failed_checks}")

    return failed_checks == 0


def run_validation():
    session = SessionLocal()

    try:
        validate_lifecycle_statuses(session)
    finally:
        session.close()


if __name__ == "__main__":
    run_validation()
