from fastapi import APIRouter, Depends

from app.core.database import SessionLocal
from app.models.contact import EmergencyContact
from app.security import require_roles


router = APIRouter(
    prefix="/contacts",
    tags=["Emergency Contacts"]
)


@router.post("/")
def add_contact(
    patient_id: int,
    name: str,
    relationship: str,
    phone: str,
    contact_type: str,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR")
    )
):
    db = SessionLocal()

    try:
        contact = EmergencyContact(
            patient_id=patient_id,
            name=name,
            relationship=relationship,
            phone=phone,
            contact_type=contact_type.upper()
        )

        db.add(contact)
        db.commit()
        db.refresh(contact)

        return {
            "success": True,
            "id": contact.id,
            "patient_id": contact.patient_id,
            "name": contact.name,
            "relationship": contact.relationship,
            "phone": contact.phone,
            "contact_type": contact.contact_type
        }

    finally:
        db.close()


@router.get("/{patient_id}")
def get_contacts(
    patient_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    db = SessionLocal()

    try:
        contacts = (
            db.query(EmergencyContact)
            .filter(
                EmergencyContact.patient_id == patient_id
            )
            .all()
        )

        return [
            {
                "id": contact.id,
                "name": contact.name,
                "relationship": contact.relationship,
                "phone": contact.phone,
                "contact_type": contact.contact_type
            }
            for contact in contacts
        ]

    finally:
        db.close()