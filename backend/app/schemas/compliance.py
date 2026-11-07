
from pydantic import BaseModel, ConfigDict


class RequirementDetail(BaseModel):
    customer_requirement_id: str
    requirement_id: str
    requirement_name: str
    document_type: str
    requirement_status: str
    document_status: str | None


class ComplianceResponse(BaseModel):
    customer_id: str
    total_requirements: int
    satisfied_requirements: int
    pending_requirements: int
    rejected_requirements: int
    waived_requirements: int
    completion_percentage: float
    compliance_status: str
    requirements: list[RequirementDetail]
