
from fastapi import FastAPI

from app.routes.customer import router as customer_router
from app.routes.document import router as document_router
from app.routes.verification import router as verification_router
from app.routes.compliance import router as compliance_router
from app.routes.risk import router as risk_router
from app.routes.review import router as review_router
from app.routes.alert import router as alert_router
from app.routes.audit import router as audit_router
from app.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="KYC Compliance Management System",
    description="Customer onboarding and compliance management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "KYC Compliance API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(customer_router)
app.include_router(document_router)
app.include_router(verification_router)
app.include_router(compliance_router)
app.include_router(risk_router)
app.include_router(review_router)
app.include_router(alert_router)
app.include_router(audit_router)
app.include_router(dashboard_router)