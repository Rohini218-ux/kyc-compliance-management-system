
import json
from pathlib import Path

from sqlalchemy import text

from app.database import SessionLocal


GROUND_TRUTH_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "ground_truth"
    / "anomalies.json"
)


def load_ground_truth():
    with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return {
        item["anomaly_id"]: item
        for item in data["anomalies"]
    }


def evaluate_anomalies(session, ground_truth):

    # Each query returns the IDs of detected anomalous records.
    detection_queries = {
        "AN-001": text("""
            SELECT DISTINCT d.document_id
            FROM documents d
            JOIN verifications v
                ON v.document_id = d.document_id
            WHERE d.status = 'VERIFIED'
              AND v.status = 'PENDING'
        """),

        
        "AN-002": text("""
        SELECT customer_id
        FROM beneficial_owners
        GROUP BY customer_id
         HAVING SUM(ownership_percentage) > 100
        """),


        "AN-003": text("""
            SELECT review_case_id
            FROM review_cases
            WHERE status = 'OVERDUE'
              AND review_due_date > CURRENT_DATE
        """),

        "AN-004": text("""
            SELECT customer_id
            FROM customers
            WHERE onboarding_date > CURRENT_DATE
        """),

        "AN-005": text("""
            SELECT cr.customer_requirement_id
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
        """),
    }

    # Normalize the ground-truth IDs to match detector output.
    expected = {}

    for anomaly_id, item in ground_truth.items():

        if anomaly_id == "AN-002":
            customer_id = session.execute(
                text("""
                    SELECT customer_id
                    FROM beneficial_owners
                    WHERE beneficial_owner_id = :owner_id
                """),
                {"owner_id": item["entity_id"]},
            ).scalar_one()

            expected[anomaly_id] = customer_id

        else:
            expected[anomaly_id] = item["entity_id"]

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    print("\nGROUND TRUTH EVALUATION")
    print("=" * 65)

    for anomaly_id, query in detection_queries.items():

        detected_ids = {
            str(row[0])
            for row in session.execute(query).fetchall()
        }

        actual_id = expected[anomaly_id]

        if actual_id in detected_ids:
            true_positives += 1
            print(f"CORRECTLY DETECTED | {anomaly_id}")
        else:
            false_negatives += 1
            print(f"MISSED | {anomaly_id}")

        extra_ids = detected_ids - {actual_id}

        false_positives += len(extra_ids)

        for extra_id in sorted(extra_ids):
            print(f"FALSE POSITIVE | {anomaly_id} | {extra_id}")

    precision = (
        true_positives / (true_positives + false_positives)
        if true_positives + false_positives else 0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if true_positives + false_negatives else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    print("\n" + "=" * 65)
    print("EVALUATION METRICS")
    print("=" * 65)
    print(f"True Positives : {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    print(f"Precision      : {precision:.2%}")
    print(f"Recall         : {recall:.2%}")
    print(f"F1 Score       : {f1_score:.2%}")


def run_evaluation():
    ground_truth = load_ground_truth()

    if len(ground_truth) != 5:
        raise ValueError("Expected exactly five ground-truth anomalies.")

    session = SessionLocal()

    try:
        evaluate_anomalies(session, ground_truth)
    finally:
        session.close()


if __name__ == "__main__":
    run_evaluation()
