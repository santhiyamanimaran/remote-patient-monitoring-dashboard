
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import SessionLocal
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.security import get_current_user, require_roles
from app.services.audit_service import create_audit_log

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)


@router.post("/")
def create_patient(
    patient: PatientCreate,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR")
    )
):
    db = SessionLocal()
    try:
        new_patient = Patient(
            name=patient.name,
            age=patient.age,
            gender=patient.gender
        )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        create_audit_log(
            user_id=int(current_user["sub"]),
            action="CREATE",
            resource="PATIENT",
            patient_id=new_patient.id
        )

        return {
            "message": "Patient created successfully",
            "patient_id": new_patient.id
        }
    finally:
        db.close()


@router.get("/")
def get_patients(
    current_user: dict = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        patients = db.query(Patient).all()

        create_audit_log(
            user_id=int(current_user["sub"]),
            action="VIEW",
            resource="PATIENT_LIST"
        )

        return patients
    finally:
        db.close()


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    current_user: dict = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        create_audit_log(
            user_id=int(current_user["sub"]),
            action="VIEW",
            resource="PATIENT",
            patient_id=patient_id
        )

        return patient
    finally:
        db.close()


@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR")
    )
):
    db = SessionLocal()
    try:
        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        update_data = patient_data.dict(
            exclude_unset=True
        )

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No patient details provided"
            )

        for field, value in update_data.items():
            setattr(patient, field, value)

        db.commit()
        db.refresh(patient)

        create_audit_log(
            user_id=int(current_user["sub"]),
            action="UPDATE",
            resource="PATIENT",
            patient_id=patient_id
        )

        return {
            "message": "Patient updated successfully",
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender
            }
        }
    finally:
        db.close()
