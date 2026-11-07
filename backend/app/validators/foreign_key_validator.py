
from sqlalchemy import text

from app.database import SessionLocal


FOREIGN_KEY_CHECKS = [
    ("customers", "customer_type_id", "customer_types", "customer_type_id"),
    ("requirement_applicability", "customer_type_id", "customer_types", "customer_type_id"),
    ("requirement_applicability", "requirement_id", "kyc_requirements", "requirement_id"),
    ("customer_requirements", "customer_id", "customers", "customer_id"),
    ("customer_requirements", "requirement_id", "kyc_requirements", "requirement_id"),
    ("documents", "customer_id", "customers", "customer_id"),
    ("documents", "customer_requirement_id", "customer_requirements", "customer_requirement_id"),
    ("verifications", "document_id", "documents", "document_id"),
    ("risk_ratings", "customer_id", "customers", "customer_id"),
    ("review_cases", "customer_id", "customers", "customer_id"),
    ("beneficial_owners", "customer_id", "customers", "customer_id"),
    ("alerts", "customer_id", "customers", "customer_id"),
]


def validate_foreign_keys():

    results = []

    with SessionLocal() as db:

        for child_table, child_column, parent_table, parent_column in FOREIGN_KEY_CHECKS:

            query = text(f"""
                SELECT COUNT(*)
                FROM {child_table} child
                LEFT JOIN {parent_table} parent
                    ON child.{child_column} = parent.{parent_column}
                WHERE child.{child_column} IS NOT NULL
                  AND parent.{parent_column} IS NULL
            """)

            orphan_count = db.execute(query).scalar()

            results.append({
                "relationship": (
                    f"{child_table}.{child_column} -> "
                    f"{parent_table}.{parent_column}"
                ),
                "orphan_count": orphan_count,
                "status": "PASS" if orphan_count == 0 else "FAIL",
            })

    for result in results:
        print(
            f"{result['relationship']:<90}"
            f"Orphans: {result['orphan_count']:<5}"
            f"{result['status']}"
        )

    return results


if __name__ == "__main__":

    results = validate_foreign_keys()

    failed = [
        result for result in results
        if result["status"] == "FAIL"
    ]

    print("\nForeign Key Validation Summary")
    print(f"Relationships checked: {len(results)}")
    print(f"Passed: {len(results) - len(failed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        raise SystemExit("Foreign key validation failed.")
