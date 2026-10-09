from sqlalchemy.orm import Session
from app.models.patient import Patient
def get_all_patients(db: Session):
    return db.query(Patient).all()
def create_patient(
    db: Session,
    name: str,
    age: int,
    gender: str
):
    patient = Patient(
        name=name,
        age=age,
        gender=gender
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient
def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()