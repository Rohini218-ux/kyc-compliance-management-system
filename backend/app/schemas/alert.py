
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AlertStatus = Literal["OPEN", "ACKNOWLEDGED", "RESOLVED"]


class AlertUpdate(BaseModel):
    status: AlertStatus
    performed_by: str = Field(min_length=1, max_length=100)
    remarks: str | None = Field(default=None, max_length=2000)


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: str
    customer_id: str
    alert_type: str
    severity: str
    status: AlertStatus
    description: str
    created_at: datetime
    resolved_at: datetime | None
