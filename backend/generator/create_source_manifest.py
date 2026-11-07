
import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

manifest = {
    "project": "KYC Compliance Management System",
    "dataset_type": "Synthetic Data",
    "dataset_seed": 20261022,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "generation_method": "Python scripts using Faker and deterministic random seed",
    "database": "PostgreSQL",
    "tables": [
        "customer_types",
        "customers",
        "kyc_requirements",
        "requirement_applicability",
        "customer_requirements",
        "documents",
        "verifications",
        "risk_ratings",
        "review_cases",
        "beneficial_owners",
        "alerts",
        "audit_events"
    ],
    "expected_record_counts": {
        "customers": 8000,
        "documents": 20000,
        "review_cases": 3000
    },
    "anomaly_injection": {
        "enabled": True,
        "ground_truth_file": "backend/data/ground_truth/anomalies.json",
        "known_anomaly_categories": 5
    },
    "privacy": {
        "contains_real_customer_data": False,
        "contains_personal_information": "Synthetic only"
    }
}

output_path = PROJECT_ROOT / "docs" / "source_manifest.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(
    json.dumps(manifest, indent=4),
    encoding="utf-8"
)

print(f"Source manifest created: {output_path}")
