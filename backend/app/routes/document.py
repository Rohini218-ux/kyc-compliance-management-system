
from uuid import uuid4
from pathlib import Path
from fastapi.responses import FileResponse
import fitz

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status
)
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document import Document
from app.models.customer import Customer
from app.models.customer_requirement import CustomerRequirement
from app.schemas.document import DocumentResponse
from app.config.storage import (
    DOCUMENT_STORAGE_DIR,
    MAX_FILE_SIZE
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_document(
    customer_id: str = Form(...),
    customer_requirement_id: str = Form(...),
    document_type: str = Form(...),
    issue_date: str | None = Form(None),
    expiry_date: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Validate customer
    customer = db.get(Customer, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # 2. Validate requirement belongs to customer
    requirement = db.get(
        CustomerRequirement,
        customer_requirement_id
    )

    if (
        requirement is None
        or requirement.customer_id != customer_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Customer requirement not found"
        )

    # 3. Validate file extension and content type
    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid content type"
        )

    # 4. Read and validate file size
    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty PDF file"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Maximum file size is 10 MB"
        )

    # 5. Validate PDF signature
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # 6. Validate PDF structure
    try:
        pdf = fitz.open(stream=content, filetype="pdf")

        if pdf.page_count == 0:
            pdf.close()
            raise HTTPException(
                status_code=400,
                detail="PDF contains no pages"
            )

        pdf.close()

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read PDF file"
        )

    # 7. Generate unique document ID
    document_id = f"DOC-{uuid4().hex[:16].upper()}"
    stored_path = DOCUMENT_STORAGE_DIR / f"{document_id}.pdf"

    # 8. Parse dates
    from datetime import date

    try:
        parsed_issue_date = (
            date.fromisoformat(issue_date) if issue_date else None
        )
        parsed_expiry_date = (
            date.fromisoformat(expiry_date) if expiry_date else None
        )

        if (
            parsed_issue_date
            and parsed_expiry_date
            and parsed_expiry_date < parsed_issue_date
        ):
            raise HTTPException(
                status_code=400,
                detail="Expiry date cannot be before issue date"
            )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Dates must use YYYY-MM-DD format"
        )

    # 9. Create database record
    document = Document(
        document_id=document_id,
        customer_id=customer_id,
        customer_requirement_id=customer_requirement_id,
        document_type=document_type,
        document_name=Path(file.filename).name,
        issue_date=parsed_issue_date,
        expiry_date=parsed_expiry_date,
        status="PENDING"
    )

    try:
        # Save PDF
        stored_path.write_bytes(content)

        # Save metadata
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    except Exception:
        db.rollback()

        if stored_path.exists():
            stored_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Unable to save document"
        )

    

    finally:
        await file.close()


@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid pagination parameters"
        )

    return (
        db.query(Document)
        .order_by(Document.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_path = (
        DOCUMENT_STORAGE_DIR / f"{document.document_id}.pdf"
    ).resolve()

    if (
        file_path.parent != DOCUMENT_STORAGE_DIR.resolve()
        or not file_path.is_file()
    ):
        raise HTTPException(
            status_code=404,
            detail="Stored PDF file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=document.document_name
    )

