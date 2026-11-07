
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


DocumentStatus = Literal[
    "PENDING",
    "VERIFIED",
    "REJECTED",
    "EXPIRED"
]


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    customer_id: str
    customer_requirement_id: str
    document_type: str
    document_name: str
    issue_date: date | None
    expiry_date: date | None
    status: DocumentStatus
    uploaded_at: datetime
