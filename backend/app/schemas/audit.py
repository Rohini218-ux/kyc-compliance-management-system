from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    audit_event_id: str
    entity_type: str
    entity_id: str
    action: str
    performed_by: str
    details: str | None
    event_timestamp: datetime