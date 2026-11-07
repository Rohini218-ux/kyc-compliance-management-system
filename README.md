# KYC Compliance Management System

A full-stack application for managing **Know Your Customer (KYC)** operations, monitoring customer compliance, verifying documents, assessing risk, and tracking review activities.

The system is designed to demonstrate how a compliance team can manage customer information and KYC requirements through a centralized platform.

## 1. Project Overview

Financial institutions and regulated businesses must verify customer identities and ensure that customers meet applicable compliance requirements.

Managing these activities manually can lead to delays, inconsistent records, and difficulty tracking outstanding verification tasks.

The **KYC Compliance Management System** addresses these challenges by providing a centralized application to:

- Maintain customer information.
- Manage KYC requirements.
- Upload and track customer documents.
- Monitor document verification.
- Evaluate customer compliance status.
- Manage risk ratings and review cases.
- Generate alerts and maintain audit records.

## 2. Key Features

### Dashboard
- View overall compliance information.
- Monitor customer and document activity.
- Track important compliance indicators.

### Customer Management
- Manage individual and business customer records.
- View customer details.
- Track customer-specific KYC information.

### Document Management
- Upload customer documents.
- Validate PDF uploads.
- Store and retrieve document information.
- Track document verification status.

### Compliance Management
- Evaluate customer KYC requirements.
- Identify satisfied and pending requirements.
- Calculate customer compliance percentages.
- Display overall compliance status.

### Risk Management
- Maintain customer risk ratings.
- Identify high-risk customers.
- Support compliance risk monitoring.

### Review Case Management
- Manage customer review cases.
- Track review status and activities.

### Alerts Management
- View and manage compliance-related alerts.
- Track alerts requiring attention.

### Audit Logs
- Maintain records of system activities.
- Support activity tracking and accountability.

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React.js, JavaScript, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Data Validation | Pydantic |
| API Testing | Postman, Swagger UI |
| Automated Testing | Pytest |
| Version Control | Git, GitHub |

## 4. System Architecture

The application follows a frontend–backend architecture.

```text
             USER
               |
               v
       React Frontend
               |
          REST APIs
               |
               v
        FastAPI Backend
               |
       Business Logic Layer
               |
               v
        SQLAlchemy ORM
               |
               v
          PostgreSQL
```

**Frontend:** Provides the user interface for customer, document, compliance, risk, review, alert, and audit operations.

**Backend:** Handles API requests, business logic, validation, and database operations.

**Database:** Stores customer information, KYC requirements, documents, verification records, risk ratings, review cases, alerts, and audit events.

## 5. Database Design

The PostgreSQL database contains the following core tables:

- `customer_types`
- `customers`
- `kyc_requirements`
- `requirement_applicability`
- `customer_requirements`
- `documents`
- `verifications`
- `risk_ratings`
- `review_cases`
- `beneficial_owners`
- `alerts`
- `audit_events`

These tables support customer onboarding, KYC requirement tracking, document management, verification, risk assessment, and compliance operations.

## 6. Project Structure

```text
Kyc_compliance_system/
│
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
│
├── docs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 7. Getting Started

### Prerequisites

Install the following before running the application:

- Python
- Node.js and npm
- PostgreSQL
- Git

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Kyc_compliance_system
```

### Step 2: Backend Setup

Create and activate a Python virtual environment if one does not already exist.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies using the appropriate requirements file.

Configure the PostgreSQL database connection using the backend application's configuration.

Run database migrations if required:

```powershell
cd backend
alembic upgrade head
```

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

Backend API:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### Step 3: Frontend Setup

Open a separate terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend application:

http://localhost:5173

## 8. Testing

The backend includes automated tests using Pytest.

Run the tests from the backend directory:

```powershell
cd backend
pytest -v
```

The test suite has been executed successfully in the development environment.

## 9. Sample Dataset

The project uses synthetic data for development and testing.

The generated dataset includes:

- 8,000 customer records.
- 20,000 document records.
- 1,000 business entities.
- 3,000 review cases.
- Five controlled anomaly test cases.

The dataset uses deterministic seed `20261022` to support repeatable testing.

The anomaly test results are based on controlled synthetic scenarios and should not be interpreted as real-world compliance detection performance.

## 10. Security and Limitations

This project is a demonstration implementation.

Before using it in a real financial or regulated environment, additional capabilities are required, including:

- User authentication and role-based access control.
- Strong data encryption and secure file storage.
- Sensitive data protection.
- Production-grade logging and monitoring.
- Regulatory and compliance validation.
- Secure deployment and backup procedures.

Do not upload real customer KYC documents, personal information, database credentials, or secret keys to a public repository.

## 11. Future Enhancements

Potential improvements include:

- AI-assisted document information extraction.
- Automated document classification.
- Intelligent compliance checks.
- Explainable risk assessment.
- Notification and workflow automation.
- Advanced analytics and reporting.
- Role-based user permissions.

## 12. Project Objective

The objective of this project is to demonstrate practical full-stack development skills, REST API design, relational database modelling, business workflow implementation, document processing, and automated testing through a real-world-inspired KYC compliance application.

---

**Project:** KYC Compliance Management System  
**Backend:** Python + FastAPI  
**Frontend:** React.js  
**Database:** PostgreSQL  
**Testing:** Pytest