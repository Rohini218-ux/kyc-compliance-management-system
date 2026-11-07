# KYC Compliance System — Data Dictionary

This document describes the database schema.


## customer_types

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| customer_type_id | character varying | NO | YES | - | - |
| type_code | character varying | NO | NO | - | - |
| type_name | character varying | NO | NO | - | - |
| description | text | YES | NO | - | - |
| is_active | boolean | NO | NO | - | - |
| effective_from | date | NO | NO | - | - |
| effective_to | date | YES | NO | - | - |

## customers

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| customer_id | character varying | NO | YES | - | - |
| customer_type_id | character varying | NO | NO | customer_types.customer_type_id | - |
| customer_name | character varying | NO | NO | - | - |
| date_of_birth | date | YES | NO | - | - |
| onboarding_date | date | NO | NO | - | - |
| status | character varying | NO | NO | - | - |
| created_at | timestamp with time zone | NO | NO | - | - |

## kyc_requirements

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| requirement_id | character varying | NO | YES | - | - |
| requirement_code | character varying | NO | NO | - | - |
| requirement_name | character varying | NO | NO | - | - |
| document_type | character varying | NO | NO | - | - |
| description | text | YES | NO | - | - |
| is_mandatory | boolean | NO | NO | - | - |
| is_active | boolean | NO | NO | - | - |
| effective_from | date | NO | NO | - | - |
| effective_to | date | YES | NO | - | - |

## requirement_applicability

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| applicability_id | integer | NO | YES | - | nextval('requirement_applicability_applicability_id_seq'::regclass) |
| customer_type_id | character varying | NO | NO | customer_types.customer_type_id | - |
| requirement_id | character varying | NO | NO | kyc_requirements.requirement_id | - |
| risk_level | character varying | NO | NO | - | - |
| is_mandatory | boolean | NO | NO | - | - |
| effective_from | date | NO | NO | - | - |
| effective_to | date | YES | NO | - | - |

## customer_requirements

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| customer_requirement_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| requirement_id | character varying | NO | NO | kyc_requirements.requirement_id | - |
| status | character varying | NO | NO | - | - |
| assigned_date | date | NO | NO | - | - |
| completed_date | date | YES | NO | - | - |

## documents

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| document_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| document_type | character varying | NO | NO | - | - |
| document_name | character varying | NO | NO | - | - |
| issue_date | date | YES | NO | - | - |
| expiry_date | date | YES | NO | - | - |
| status | character varying | NO | NO | - | - |
| uploaded_at | timestamp with time zone | NO | NO | - | - |
| customer_requirement_id | character varying | NO | NO | customer_requirements.customer_requirement_id | - |

## verifications

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| verification_id | character varying | NO | YES | - | - |
| document_id | character varying | NO | NO | documents.document_id | - |
| verification_type | character varying | NO | NO | - | - |
| status | character varying | NO | NO | - | - |
| remarks | text | YES | NO | - | - |
| verified_at | timestamp with time zone | YES | NO | - | - |
| created_at | timestamp with time zone | NO | NO | - | - |

## risk_ratings

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| risk_rating_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| risk_level | character varying | NO | NO | - | - |
| reason | text | YES | NO | - | - |
| effective_from | date | NO | NO | - | - |
| effective_to | date | YES | NO | - | - |
| created_at | timestamp with time zone | NO | NO | - | - |

## review_cases

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| review_case_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| review_type | character varying | NO | NO | - | - |
| review_due_date | date | NO | NO | - | - |
| completed_date | date | YES | NO | - | - |
| status | character varying | NO | NO | - | - |
| remarks | text | YES | NO | - | - |
| created_at | timestamp with time zone | NO | NO | - | - |

## beneficial_owners

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| beneficial_owner_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| owner_name | character varying | NO | NO | - | - |
| ownership_percentage | numeric | NO | NO | - | - |
| effective_from | date | NO | NO | - | - |
| effective_to | date | YES | NO | - | - |

## alerts

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| alert_id | character varying | NO | YES | - | - |
| customer_id | character varying | NO | NO | customers.customer_id | - |
| alert_type | character varying | NO | NO | - | - |
| severity | character varying | NO | NO | - | - |
| status | character varying | NO | NO | - | - |
| description | text | NO | NO | - | - |
| created_at | timestamp with time zone | NO | NO | - | - |
| resolved_at | timestamp with time zone | YES | NO | - | - |

## audit_events

| Column | Data Type | Nullable | PK | FK Reference | Default |
|---|---|---|---|---|---|
| audit_event_id | character varying | NO | YES | - | - |
| entity_type | character varying | NO | NO | - | - |
| entity_id | character varying | NO | NO | - | - |
| action | character varying | NO | NO | - | - |
| performed_by | character varying | NO | NO | - | - |
| details | text | YES | NO | - | - |
| event_timestamp | timestamp with time zone | NO | NO | - | - |