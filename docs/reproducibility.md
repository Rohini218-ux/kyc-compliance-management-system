# KYC Compliance Management System — Reproducibility Guide

## 1. Project Overview

This project generates a synthetic KYC compliance dataset for testing customer onboarding, document verification, risk assessment, periodic reviews, and anomaly detection.

No real customer data is used.

## 2. Dataset Configuration

- Dataset seed: `20261022`
- Database: PostgreSQL
- Backend: Python and FastAPI
- ORM: SQLAlchemy
- Migration tool: Alembic
- Synthetic data generator: Faker
- Total business tables: 12

## 3. Environment Setup

1. Install Python and PostgreSQL.
2. Clone the project repository.
3. Create and activate a virtual environment.
4. Install dependencies from `requirements.txt`.
5. Create the PostgreSQL database.
6. Configure database credentials in the backend `.env` file.

## 4. Database Setup

Run the following commands from the backend directory:

```bash
alembic upgrade head
```

This creates the database schema using the migration history.

## 5. Data Generation

Run the data generation scripts in this order:

1. `seed_reference_data.py`
2. `generate_customers.py`
3. `generate_risk_ratings.py`
4. `generate_customer_requirements.py`
5. `generate_documents.py`
6. `generate_verifications.py`
7. `generate_review_cases.py`
8. `generate_beneficial_owners.py`
9. `generate_alerts.py`
10. `generate_audit_events.py`

The configured seed is `20261022`.

## 6. Data Validation

Run the validation scripts to check:

- Primary key uniqueness
- Foreign key integrity
- Required fields
- Date and arithmetic rules
- Lifecycle status rules
- Document and verification consistency
- KYC completeness
- Review and ownership rules

## 7. Anomaly Injection

Run the anomaly injection process separately after generating and validating the clean baseline.

Five controlled anomaly categories are included:

1. Document-verification mismatch
2. Beneficial ownership exceeding 100% in aggregate
3. Overdue review with a future due date
4. Future customer onboarding date
5. Satisfied requirement without a verified document

The anomaly ground truth is stored separately in:

`backend/data/ground_truth/anomalies.json`

## 8. Exported Deliverables

Exports are organized by dataset version.

- CSV exports
- JSON exports
- PostgreSQL SQL dump
- PostgreSQL custom-format backup
- Data dictionary
- Source manifest
- Validation summary
- SHA-256 checksum manifest

## 9. Integrity Verification

The file `docs/checksums.json` contains SHA-256 hashes for the exported anomaly-injected dataset files.

Recalculate the checksums after any export changes and compare them with the previous manifest.

## 10. Reproducibility Notes

Use the same seed, dependency versions, database schema, and generation order to reproduce the dataset.

Database-generated identifiers, timestamps, or environment differences may affect byte-for-byte reproducibility unless they are also controlled.

The clean baseline and anomaly-injected dataset must be maintained separately. Do not treat an anomaly-injected export as clean data.