
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models.patient import Patient
from app.models.vital import VitalReading
from app.models.alert import Alert
from app.models.contact import EmergencyContact
from app.models.notification import Notification
from app.models.user import User
from app.models.audit_log import AuditLog

from app.api.patients import router as patient_router
from app.vitals.routes import router as vital_router
from app.api.alerts import router as alert_router
from app.api.contact import router as contact_router
from app.api.auth import router as auth_router
from app.api.notifications import router as notification_router


app = FastAPI(
    title="Remote Patient Monitoring System",
    version="1.0.0",
    description="Backend API for remote patient health monitoring"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register API routes
app.include_router(patient_router)
app.include_router(vital_router)
app.include_router(alert_router)
app.include_router(contact_router)
app.include_router(auth_router)
app.include_router(notification_router)


@app.get("/")
def home():
    return {
        "success": True,
        "data": None,
        "message": "Remote Patient Monitoring API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

