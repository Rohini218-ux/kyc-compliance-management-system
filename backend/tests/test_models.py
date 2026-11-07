from app.database import Base

from app.models import (
    CustomerType,
    Customer,
    KYCRequirement,
    RequirementApplicability,
    Document,
    Verification,
    RiskRating,
    ReviewCase,
    BeneficialOwner,
    Alert,
    AuditEvent,
    CustomerRequirement
)

def test_document_table_exists():
    assert "documents" in Base.metadata.tables


def test_document_customer_foreign_key():
    table = Document.__table__

    assert "customer_id" in table.c
    assert len(table.c.customer_id.foreign_keys) == 1


def test_kyc_requirement_table_exists():
    assert "kyc_requirements" in Base.metadata.tables


def test_requirement_applicability_table_exists():
    assert "requirement_applicability" in Base.metadata.tables


def test_applicability_foreign_keys():

    table = RequirementApplicability.__table__

    assert "customer_type_id" in table.c
    assert "requirement_id" in table.c

    assert len(table.c.customer_type_id.foreign_keys) == 1
    assert len(table.c.requirement_id.foreign_keys) == 1


def test_requirement_primary_key():

    table = KYCRequirement.__table__

    assert table.primary_key.columns.keys() == ["requirement_id"]

def test_verification_table_exists():
    assert "verifications" in Base.metadata.tables

def test_verification_document_foreign_key():
    table = Verification.__table__

    assert "document_id" in table.c
    assert len(table.c.document_id.foreign_keys) == 1 
def test_risk_rating_table_exists():
    assert "risk_ratings" in Base.metadata.tables


def test_risk_rating_customer_foreign_key():
    table = RiskRating.__table__

    assert "customer_id" in table.c
    assert len(table.c.customer_id.foreign_keys) == 1   

def test_review_case_table_exists():
    assert "review_cases" in Base.metadata.tables


def test_review_case_customer_foreign_key():
    table = ReviewCase.__table__

    assert "customer_id" in table.c
    assert len(table.c.customer_id.foreign_keys) == 1   

def test_beneficial_owner_table_exists():
    assert "beneficial_owners" in Base.metadata.tables


def test_beneficial_owner_customer_foreign_key():
    table = BeneficialOwner.__table__

    assert "customer_id" in table.c
    assert len(table.c.customer_id.foreign_keys) == 1


def test_beneficial_owner_percentage_constraint():
    table = BeneficialOwner.__table__

    constraints = [
        constraint.name
        for constraint in table.constraints
    ]

    assert "check_ownership_percentage" in constraints    

def test_alert_table_exists():
    assert "alerts" in Base.metadata.tables


def test_alert_customer_foreign_key():
    table = Alert.__table__

    assert "customer_id" in table.c
    assert len(table.c.customer_id.foreign_keys) == 1


def test_alert_constraints():
    table = Alert.__table__

    constraints = [
        constraint.name
        for constraint in table.constraints
    ]

    assert "check_alert_severity" in constraints
    assert "check_alert_status" in constraints  

def test_audit_event_table_exists():
    assert "audit_events" in Base.metadata.tables


def test_audit_event_required_columns():
    table = AuditEvent.__table__

    assert "entity_type" in table.c
    assert "entity_id" in table.c
    assert "action" in table.c
    assert "performed_by" in table.c
    assert "event_timestamp" in table.c    

def test_customer_requirement_table_exists():
    assert "customer_requirements" in Base.metadata.tables


def test_customer_requirement_foreign_keys():
    table = CustomerRequirement.__table__

    assert "customer_id" in table.c
    assert "requirement_id" in table.c

    assert len(table.c.customer_id.foreign_keys) == 1
    assert len(table.c.requirement_id.foreign_keys) == 1


def test_customer_requirement_unique_constraint():
    table = CustomerRequirement.__table__

    constraints = [
        constraint.name
        for constraint in table.constraints
    ]

    assert "uq_customer_requirement" in constraints      