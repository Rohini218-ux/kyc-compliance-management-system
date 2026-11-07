
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CustomerStatus = Literal[
    "ONBOARDING",
    "PENDING",
    "APPROVED",
    "REJECTED",
    "SUSPENDED"
]


class CustomerCreate(BaseModel):
    customer_type_id: str = Field(min_length=1, max_length=10)
    customer_name: str = Field(min_length=1, max_length=150)
    date_of_birth: date | None = None
    onboarding_date: date
    status: CustomerStatus = "ONBOARDING"


class CustomerUpdate(BaseModel):
    customer_type_id: str | None = Field(
        default=None, min_length=1, max_length=10
    )
    customer_name: str | None = Field(
        default=None, min_length=1, max_length=150
    )
    date_of_birth: date | None = None
    onboarding_date: date | None = None
    status: CustomerStatus | None = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    customer_type_id: str
    customer_name: str
    date_of_birth: date | None
    onboarding_date: date
    status: str
    created_at: datetime
