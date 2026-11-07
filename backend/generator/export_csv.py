
import csv
from pathlib import Path

from sqlalchemy import text

from app.database import engine


# Export all 12 business tables
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


def export_table(connection, table_name, output_dir):

    query = text(f'SELECT * FROM "{table_name}"')

    result = connection.execute(query)

    columns = list(result.keys())

    file_path = output_dir / f"{table_name}.csv"

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(columns)

        row_count = 0

        for row in result:
            writer.writerow(row)
            row_count += 1

    print(f"EXPORTED | {table_name} | {row_count} rows")

    return row_count


def export_csv(dataset_version):

    if dataset_version not in ["clean", "anomaly_injected"]:
        raise ValueError("Invalid dataset version")

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "exports"
        / dataset_version
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    total_rows = 0

    with engine.connect() as connection:

        for table in TABLES:
            total_rows += export_table(
                connection,
                table,
                output_dir
            )

    print("\n" + "=" * 55)
    print("CSV EXPORT SUMMARY")
    print("=" * 55)
    print(f"Dataset version: {dataset_version}")
    print(f"Tables exported: {len(TABLES)}")
    print(f"Total rows exported: {total_rows}")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":

    export_csv("anomaly_injected")
