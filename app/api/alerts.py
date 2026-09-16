from fastapi import APIRouter, Depends

from app.core.database import SessionLocal
from app.models.alert import Alert
from app.security import require_roles


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/{patient_id}")
def get_patient_alerts(
    patient_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    db = SessionLocal()

    try:
        alerts = (
            db.query(Alert)
            .filter(Alert.patient_id == patient_id)
            .order_by(Alert.created_at.desc())
            .all()
        )

        return [
            {
                "id": alert.id,
                "patient_id": alert.patient_id,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "severity": alert.severity,
                "created_at": alert.created_at.isoformat(),
            }
            for alert in alerts
        ]

    finally:
        db.close()