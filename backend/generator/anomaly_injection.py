
import json
from pathlib import Path
from datetime import datetime, timezone

from sqlalchemy import text

from app.database import SessionLocal


GROUND_TRUTH_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ground_truth"
)

GROUND_TRUTH_FILE = GROUND_TRUTH_DIR / "anomalies.json"


def inject_anomalies():
    GROUND_TRUTH_DIR.mkdir(parents=True, exist_ok=True)

    if GROUND_TRUTH_FILE.exists():
        raise FileExistsError(
            "Ground-truth file already exists. "
            "Do not inject anomalies again."
        )

    session = SessionLocal()
    records = []

    try:
        # AN-001: Document and verification mismatch
        document = session.execute(text("""
            SELECT d.document_id, d.status, v.status AS verification_status
            FROM documents d
            JOIN verifications v
                ON v.document_id = d.document_id
            WHERE d.status = 'VERIFIED'
              AND v.status = 'VERIFIED'
            LIMIT 1
        """)).mappings().first()

        if not document:
            raise ValueError("No suitable document found for AN-001")

        records.append({
            "anomaly_id": "AN-001",
            "entity_type": "document",
            "entity_id": document["document_id"],
            "anomaly_type": "DOCUMENT_VERIFICATION_MISMATCH",
            "original_value": {
                "document_status": document["status"],
                "verification_status": document["verification_status"],
            },
            "injected_value": {
                "document_status": "VERIFIED",
                "verification_status": "PENDING",
            },
        })

        # AN-002: Beneficial ownership above 100%
        ownership = session.execute(text("""
            SELECT customer_id, SUM(ownership_percentage) AS total
            FROM beneficial_owners
            GROUP BY customer_id
            HAVING SUM(ownership_percentage) = 100
            LIMIT 1
        """)).mappings().first()

        if not ownership:
            raise ValueError("No suitable ownership record found")

        
        # AN-002: Combined beneficial ownership above 100%

        owner = session.execute(text("""
            SELECT
                bo.customer_id,
                bo.beneficial_owner_id,
                bo.ownership_percentage
            FROM beneficial_owners bo
            JOIN (
                SELECT customer_id
                FROM beneficial_owners
                GROUP BY customer_id
                HAVING COUNT(*) >= 2
                   AND SUM(ownership_percentage) = 100
            ) valid_customers
                ON valid_customers.customer_id = bo.customer_id
            WHERE bo.ownership_percentage <= 90
            ORDER BY bo.customer_id, bo.beneficial_owner_id
            LIMIT 1
        """)).mappings().first()

        if not owner:
            raise ValueError(
                "No suitable multi-owner customer found for AN-002"
            )

        records.append({
            "anomaly_id": "AN-002",
            "entity_type": "beneficial_owner",
            "entity_id": owner["beneficial_owner_id"],
            "anomaly_type": "OWNERSHIP_TOTAL_OVER_100_PERCENT",
            "original_value": str(owner["ownership_percentage"]),
            "injected_value": str(
                owner["ownership_percentage"] + 10
            ),
        })


        # AN-003: Overdue review with future due date
        review = session.execute(text("""
            SELECT review_case_id, review_due_date, status
            FROM review_cases
            WHERE status = 'OVERDUE'
            LIMIT 1
        """)).mappings().first()

        if not review:
            raise ValueError("No overdue review found for AN-003")

        records.append({
            "anomaly_id": "AN-003",
            "entity_type": "review_case",
            "entity_id": review["review_case_id"],
            "anomaly_type": "OVERDUE_REVIEW_WITH_FUTURE_DATE",
            "original_value": str(review["review_due_date"]),
            "injected_value": "2099-12-31",
        })

        # AN-004: Customer onboarding date in the future
        customer = session.execute(text("""
            SELECT customer_id, onboarding_date
            FROM customers
            WHERE onboarding_date <= CURRENT_DATE
            LIMIT 1
        """)).mappings().first()

        if not customer:
            raise ValueError("No suitable customer found for AN-004")

        records.append({
            "anomaly_id": "AN-004",
            "entity_type": "customer",
            "entity_id": customer["customer_id"],
            "anomaly_type": "FUTURE_ONBOARDING_DATE",
            "original_value": str(customer["onboarding_date"]),
            "injected_value": "2099-12-31",
        })

        # AN-005: Satisfied requirement without verified document
        requirement = session.execute(text("""
            SELECT cr.customer_requirement_id, cr.status
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
            LIMIT 1
        """)).mappings().first()

        if not requirement:
            requirement = session.execute(text("""
                SELECT cr.customer_requirement_id, cr.status
                FROM customer_requirements cr
                WHERE cr.status = 'PENDING'
                LIMIT 1
            """)).mappings().first()

        if not requirement:
            raise ValueError("No suitable requirement found for AN-005")

        records.append({
            "anomaly_id": "AN-005",
            "entity_type": "customer_requirement",
            "entity_id": requirement["customer_requirement_id"],
            "anomaly_type": "SATISFIED_WITHOUT_VERIFIED_DOCUMENT",
            "original_value": requirement["status"],
            "injected_value": "SATISFIED",
        })

        # Write ground truth before modifying database.
        # If any update fails, roll back the database changes.
        payload = {
            "dataset_seed": 20261022,
            "injected_at": datetime.now(timezone.utc).isoformat(),
            "anomalies": records,
        }

        updates = [
            text("""
                UPDATE verifications
                SET status = 'PENDING'
                WHERE document_id = :document_id
                  AND status = 'VERIFIED'
            """),
            text("""
                UPDATE beneficial_owners
                SET ownership_percentage = ownership_percentage + 10
                WHERE beneficial_owner_id = :owner_id
            """),
            text("""
                UPDATE review_cases
                SET review_due_date = '2099-12-31'
                WHERE review_case_id = :review_id
            """),
            text("""
                UPDATE customers
                SET onboarding_date = '2099-12-31'
                WHERE customer_id = :customer_id
            """),
            text("""
                UPDATE customer_requirements
                SET status = 'SATISFIED'
                WHERE customer_requirement_id = :requirement_id
            """),
        ]

        params = [
            {"document_id": document["document_id"]},
            {"owner_id": owner["beneficial_owner_id"]},
            {"review_id": review["review_case_id"]},
            {"customer_id": customer["customer_id"]},
            {"requirement_id": requirement["customer_requirement_id"]},
        ]

        for query, values in zip(updates, params):
            result = session.execute(query, values)

            if result.rowcount != 1:
                raise RuntimeError(
                    "An anomaly update did not affect exactly one row."
                )

        session.commit()

        GROUND_TRUTH_FILE.write_text(
            json.dumps(payload, indent=4),
            encoding="utf-8",
        )

        print("Successfully injected 5 anomalies.")
        print(f"Ground truth saved at: {GROUND_TRUTH_FILE}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    inject_anomalies()
