
import random
from datetime import datetime, timezone, timedelta

from app.database import SessionLocal
from app.models import Document, Verification

SEED = 20261022
random.seed(SEED)

REMARKS = {
    "VERIFIED": "Document passed verification checks",
    "REJECTED": "Document failed verification checks",
    "PENDING": "Document is awaiting verification",
    "EXPIRED": "Document has expired and requires renewal",
}


def main():

    with SessionLocal() as db:
        try:
            documents = (
                db.query(Document)
                .order_by(Document.document_id)
                .all()
            )

            if not documents:
                raise ValueError("No documents found.")

            if db.query(Verification).first():
                raise ValueError(
                    "Verification records already exist."
                )

            verifications = []
            verification_counter = 1

            for document in documents:

                attempts = 2 if document.status == "REJECTED" else 1

                for attempt in range(attempts):

                    if attempt == 0:
                     if document.status == "EXPIRED":
                       status = "REJECTED"
                     else:
                        status = document.status
                    else:
                        status = random.choice(["VERIFIED", "REJECTED"])

                    created_at = (
                        document.uploaded_at
                        + timedelta(days=attempt + 1)
                    )

                    verified_at = (
                        created_at
                        if status in ("VERIFIED", "REJECTED")
                        else None
                    )

                    verifications.append(
                        Verification(
                            verification_id=(
                                f"VER-{verification_counter:08d}"
                            ),
                            document_id=document.document_id,
                            verification_type="DOCUMENT_REVIEW",
                            status=status,
                            remarks=REMARKS[status],
                            verified_at=verified_at,
                            created_at=created_at,
                        )
                    )

                    verification_counter += 1

            db.add_all(verifications)
            db.commit()

            print("Verification generation successful!")
            print(f"Documents processed: {len(documents)}")
            print(f"Verification records: {len(verifications)}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
