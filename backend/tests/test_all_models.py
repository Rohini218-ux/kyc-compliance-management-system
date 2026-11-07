from app.database import Base
from app import models


def test_all_expected_tables_registered():

    expected_tables = {
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
    }

    actual_tables = set(Base.metadata.tables.keys())

    assert expected_tables.issubset(actual_tables)