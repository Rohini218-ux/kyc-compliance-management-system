
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ReviewStatus = Literal[
    "OPEN",
    "IN_PROGRESS",
    "COMPLETED",
    "OVERDUE",
    "CANCELLED"
]


class ReviewUpdate(BaseModel):
    status: ReviewStatus
    remarks: str | None = Field(default=None, max_length=2000)


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_case_id: str
    customer_id: str
    review_type: str
    review_due_date: date
    completed_date: date | None
    status: ReviewStatus
    remarks: str | None
    created_at: datetime
