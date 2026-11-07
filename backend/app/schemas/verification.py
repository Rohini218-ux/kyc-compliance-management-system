
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


VerificationStatus = Literal["VERIFIED", "REJECTED"]


class VerificationCreate(BaseModel):
    verification_type: str = Field(min_length=1, max_length=50)
    status: VerificationStatus
    remarks: str | None = None
    performed_by: str = Field(min_length=1, max_length=100)


class VerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    verification_id: str
    document_id: str
    verification_type: str
    status: str
    remarks: str | None
    verified_at: datetime | None
    created_at: datetime
