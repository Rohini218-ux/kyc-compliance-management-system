
from pathlib import Path

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


def generate_data_dictionary():
    output_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "data_dictionary.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with engine.connect() as connection:
        lines = [
            "# KYC Compliance System — Data Dictionary\n",
            "This document describes the database schema.\n",
        ]

        for table in TABLES:
            columns = connection.execute(
                text("""
                    SELECT
                        c.column_name,
                        c.data_type,
                        c.is_nullable,
                        c.column_default,
                        CASE WHEN pk.column_name IS NOT NULL
                            THEN 'YES' ELSE 'NO' END AS is_primary_key,
                        fk.foreign_table,
                        fk.foreign_column
                    FROM information_schema.columns c
                    LEFT JOIN (
                        SELECT kcu.table_name, kcu.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                          ON tc.constraint_name = kcu.constraint_name
                         AND tc.table_schema = kcu.table_schema
                        WHERE tc.constraint_type = 'PRIMARY KEY'
                          AND tc.table_schema = 'public'
                    ) pk
                      ON pk.table_name = c.table_name
                     AND pk.column_name = c.column_name
                    LEFT JOIN (
                        SELECT
                            kcu.table_name,
                            kcu.column_name,
                            ccu.table_name AS foreign_table,
                            ccu.column_name AS foreign_column
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                          ON tc.constraint_name = kcu.constraint_name
                         AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage ccu
                          ON ccu.constraint_name = tc.constraint_name
                         AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY'
                          AND tc.table_schema = 'public'
                    ) fk
                      ON fk.table_name = c.table_name
                     AND fk.column_name = c.column_name
                    WHERE c.table_schema = 'public'
                      AND c.table_name = :table
                    ORDER BY c.ordinal_position
                """),
                {"table": table},
            ).mappings().all()

            lines.append(f"\n## {table}\n")
            lines.append(
                "| Column | Data Type | Nullable | PK | FK Reference | Default |"
            )
            lines.append(
                "|---|---|---|---|---|---|"
            )

            for column in columns:
                fk_reference = (
                    f"{column['foreign_table']}.{column['foreign_column']}"
                    if column["foreign_table"]
                    else "-"
                )
                default = column["column_default"] or "-"
                lines.append(
                    f"| {column['column_name']} "
                    f"| {column['data_type']} "
                    f"| {column['is_nullable']} "
                    f"| {column['is_primary_key']} "
                    f"| {fk_reference} "
                    f"| {default} |"
                )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Data dictionary created: {output_path}")


if __name__ == "__main__":
    generate_data_dictionary()
