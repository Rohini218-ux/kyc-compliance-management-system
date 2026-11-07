
from sqlalchemy import text

from app.database import SessionLocal


TABLES = [
    ("customer_types", "customer_type_id"),
    ("customers", "customer_id"),
    ("kyc_requirements", "requirement_id"),
    ("requirement_applicability", "applicability_id"),
    ("customer_requirements", "customer_requirement_id"),
    ("documents", "document_id"),
    ("verifications", "verification_id"),
    ("risk_ratings", "risk_rating_id"),
    ("review_cases", "review_case_id"),
    ("beneficial_owners", "beneficial_owner_id"),
    ("alerts", "alert_id"),
    ("audit_events", "audit_event_id"),
]


def validate_primary_keys():

    results = []

    with SessionLocal() as db:

        for table_name, primary_key in TABLES:

            query = text(f"""
                SELECT
                    COUNT(*) AS total_records,
                    COUNT(DISTINCT {primary_key}) AS unique_ids,
                    COUNT(*) FILTER (
                        WHERE {primary_key} IS NULL
                    ) AS null_ids
                FROM {table_name}
            """)

            result = db.execute(query).mappings().one()

            total = result["total_records"]
            unique = result["unique_ids"]
            nulls = result["null_ids"]

            duplicates = total - unique

            passed = duplicates == 0 and nulls == 0

            results.append({
                "table": table_name,
                "total": total,
                "duplicates": duplicates,
                "null_ids": nulls,
                "status": "PASS" if passed else "FAIL",
            })

    for result in results:
        print(
            f"{result['table']:<30}"
            f"Records: {result['total']:<8}"
            f"Duplicates: {result['duplicates']:<5}"
            f"Null IDs: {result['null_ids']:<5}"
            f"{result['status']}"
        )

    return results


if __name__ == "__main__":
    results = validate_primary_keys()

    failed = [
        result for result in results
        if result["status"] == "FAIL"
    ]

    print("\nPrimary Key Validation Summary")
    print(f"Tables checked: {len(results)}")
    print(f"Passed: {len(results) - len(failed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        raise SystemExit("Primary key validation failed.")
