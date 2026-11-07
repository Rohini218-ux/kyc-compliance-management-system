
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class RiskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    risk_rating_id: str
    customer_id: str
    risk_level: str
    reason: str | None
    effective_from: date
    effective_to: date | None
    created_at: datetime


class CustomerRiskResponse(BaseModel):
    customer_id: str
    customer_name: str
    customer_status: str
    risk_level: str
    reason: str | None
    effective_from: date
    effective_to: date | None
