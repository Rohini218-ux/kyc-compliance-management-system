
import json
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import text
from app.database import engine


TABLES = [
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
    "audit_events",
]


def json_serializer(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    raise TypeError(f"Unsupported type: {type(value)}")


def export_json(dataset_version="anomaly_injected"):

    if dataset_version not in ["clean", "anomaly_injected"]:
        raise ValueError("Invalid dataset version")

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "exports"
        / dataset_version
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    with engine.connect() as connection:

        for table in TABLES:

            result = connection.execute(
                text(f'SELECT * FROM "{table}"')
            )

            columns = list(result.keys())

            records = [
                dict(zip(columns, row))
                for row in result
            ]

            file_path = output_dir / f"{table}.json"

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    records,
                    file,
                    indent=4,
                    default=json_serializer
                )

            print(f"EXPORTED | {table} | {len(records)} records")

    print("\nJSON EXPORT COMPLETED")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    export_json()
