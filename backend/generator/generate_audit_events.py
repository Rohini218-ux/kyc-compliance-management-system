
from datetime import datetime, time, timezone

from app.database import SessionLocal
from app.models import (
    Customer,
    Document,
    Verification,
    RiskRating,
    ReviewCase,
    BeneficialOwner,
    Alert,
    AuditEvent,
)

BATCH_SIZE = 2000


def main():

    with SessionLocal() as db:
        try:
            if db.query(AuditEvent).first():
                raise ValueError("Audit events already exist.")

            event_counter = 1
            batch = []

            def add_event(
                entity_type,
                entity_id,
                action,
                event_timestamp,
                details,
            ):
                nonlocal event_counter, batch

                batch.append(
                    AuditEvent(
                        audit_event_id=f"AUD-{event_counter:08d}",
                        entity_type=entity_type,
                        entity_id=entity_id,
                        action=action,
                        performed_by="SYSTEM",
                        details=details,
                        event_timestamp=event_timestamp,
                    )
                )

                event_counter += 1

                if len(batch) >= BATCH_SIZE:
                    db.add_all(batch)
                    db.flush()
                    batch.clear()

            # 1. Customer creation events
            for customer in db.query(Customer).yield_per(1000):
                add_event(
                    "CUSTOMER",
                    customer.customer_id,
                    "CREATED",
                    customer.created_at,
                    "Customer record created",
                )

            # 2. Document upload events
            for document in db.query(Document).yield_per(1000):
                add_event(
                    "DOCUMENT",
                    document.document_id,
                    "UPLOADED",
                    document.uploaded_at,
                    "Customer document uploaded",
                )

            # 3. Verification events
            for verification in db.query(Verification).yield_per(1000):
                add_event(
                    "VERIFICATION",
                    verification.verification_id,
                    "VERIFICATION_RECORDED",
                    verification.created_at,
                    f"Verification status: {verification.status}",
                )

            # 4. Risk rating events
            for rating in db.query(RiskRating).yield_per(1000):
                add_event(
                    "RISK_RATING",
                    rating.risk_rating_id,
                    "ASSIGNED",
                    rating.created_at,
                    f"Risk level assigned: {rating.risk_level}",
                )

            # 5. Review case events
            for review in db.query(ReviewCase).yield_per(1000):
                add_event(
                    "REVIEW_CASE",
                    review.review_case_id,
                    "CREATED",
                    review.created_at,
                    f"Review status: {review.status}",
                )

            # 6. Beneficial owner events
            for owner in db.query(BeneficialOwner).yield_per(1000):
                event_time = datetime.combine(
                    owner.effective_from,
                    time(hour=10),
                    tzinfo=timezone.utc,
                )

                add_event(
                    "BENEFICIAL_OWNER",
                    owner.beneficial_owner_id,
                    "RECORDED",
                    event_time,
                    f"Ownership percentage: {owner.ownership_percentage}",
                )

            # 7. Alert generation events
            for alert in db.query(Alert).yield_per(1000):
                add_event(
                    "ALERT",
                    alert.alert_id,
                    "GENERATED",
                    alert.created_at,
                    f"Alert type: {alert.alert_type}",
                )

            # Insert remaining records
            if batch:
                db.add_all(batch)

            db.commit()

            print("Audit event generation successful!")
            print(f"Total audit events: {event_counter - 1}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
