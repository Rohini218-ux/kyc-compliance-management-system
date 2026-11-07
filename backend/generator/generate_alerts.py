
from datetime import date, datetime, timezone

from app.database import SessionLocal
from app.models import (
    Customer,
    Document,
    ReviewCase,
    RiskRating,
    Alert,
)

TODAY = date(2026, 11, 5)


def main():

    with SessionLocal() as db:
        try:
            if db.query(Alert).first():
                raise ValueError("Alerts already exist.")

            alerts = []
            alert_counter = 1

            def add_alert(customer_id, alert_type, severity, description):
                nonlocal alert_counter

                alerts.append(
                    Alert(
                        alert_id=f"ALT-{alert_counter:08d}",
                        customer_id=customer_id,
                        alert_type=alert_type,
                        severity=severity,
                        status="OPEN",
                        description=description,
                        created_at=datetime.now(timezone.utc),
                        resolved_at=None,
                    )
                )

                alert_counter += 1

            # 1. Expired documents
            expired_documents = (
                db.query(Document)
                .filter(Document.expiry_date < TODAY)
                .all()
            )

            for document in expired_documents:
                add_alert(
                    document.customer_id,
                    "DOCUMENT_EXPIRED",
                    "HIGH",
                    f"Document {document.document_id} has expired.",
                )

            # 2. Overdue review cases
            overdue_reviews = (
                db.query(ReviewCase)
                .filter(
                    ReviewCase.review_due_date < TODAY,
                    ReviewCase.status.in_(["OPEN", "IN_PROGRESS"]),
                )
                .all()
            )

            for review in overdue_reviews:
                add_alert(
                    review.customer_id,
                    "KYC_REVIEW_OVERDUE",
                    "HIGH",
                    f"Review {review.review_case_id} is overdue.",
                )

            # 3. High-risk customers
            high_risk_customers = (
                db.query(RiskRating)
                .filter(RiskRating.risk_level == "HIGH")
                .all()
            )

            for rating in high_risk_customers:
                add_alert(
                    rating.customer_id,
                    "HIGH_RISK_CUSTOMER",
                    "MEDIUM",
                    "Customer has a high risk rating.",
                )

            # 4. Rejected documents
            rejected_documents = (
                db.query(Document)
                .filter(Document.status == "REJECTED")
                .all()
            )

            for document in rejected_documents:
                add_alert(
                    document.customer_id,
                    "DOCUMENT_REJECTED",
                    "MEDIUM",
                    f"Document {document.document_id} was rejected.",
                )

            db.add_all(alerts)
            db.commit()

            print("Alert generation successful!")
            print(f"Expired document alerts: {len(expired_documents)}")
            print(f"Overdue review alerts: {len(overdue_reviews)}")
            print(f"High-risk alerts: {len(high_risk_customers)}")
            print(f"Rejected document alerts: {len(rejected_documents)}")
            print(f"Total alerts generated: {len(alerts)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
