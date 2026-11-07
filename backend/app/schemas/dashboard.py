from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_customers: int
    approved_customers: int
    pending_customers: int
    total_documents: int
    pending_documents: int
    verified_documents: int
    rejected_documents: int
    high_risk_customers: int
    open_alerts: int
    overdue_reviews: int