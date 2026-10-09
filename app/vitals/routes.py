from fastapi import APIRouter, Depends

from app.security import require_roles
from app.vitals.schemas import VitalReadingCreate
from app.vitals.service import save_vital_reading, get_patient_vitals


router = APIRouter(
    prefix="/vitals",
    tags=["Vital Readings"]
)


@router.post("/")
def create_vital_reading(
    data: VitalReadingCreate,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR")
    )
):
    return save_vital_reading(data)


@router.get("/{patient_id}")
def get_vitals(
    patient_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    return get_patient_vitals(patient_id)