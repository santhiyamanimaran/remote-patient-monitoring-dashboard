from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import SessionLocal
from app.models.notification import Notification
from app.security import require_roles
router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)
@router.get("/{patient_id}")
def get_patient_notifications(
    patient_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    db = SessionLocal()
    try:
        notifications = (
            db.query(Notification)
            .filter(
                Notification.patient_id == patient_id
            )
            .order_by(
                Notification.created_at.desc()
            )
            .all()
        )
        return [
            {
                "id": notification.id,
                "patient_id": notification.patient_id,
                "alert_id": notification.alert_id,
                "contact_id": notification.contact_id,
                "message": notification.message,
                "status": notification.status,
                "created_at": notification.created_at.isoformat(),
                "sent_at": (
                    notification.sent_at.isoformat()
                    if notification.sent_at
                    else None
                ),
                "acknowledged_at": (
                    notification.acknowledged_at.isoformat()
                    if notification.acknowledged_at
                    else None
                ),
            }
            for notification in notifications
        ]
    finally:
        db.close()
@router.put("/{notification_id}/send")
def send_notification(
    notification_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    db = SessionLocal()
    try:
        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id
            )
            .first()
        )
        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found"
            )
        if notification.status != "PENDING":
            raise HTTPException(
                status_code=400,
                detail="Only PENDING notifications can be sent"
            )
        notification.status = "SENT"
        notification.sent_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(notification)
        return {
            "success": True,
            "message": "Notification sent successfully",
            "notification_id": notification.id,
            "status": notification.status,
            "sent_at": notification.sent_at.isoformat()
        }
    finally:
        db.close()
@router.put("/{notification_id}/acknowledge")
def acknowledge_notification(
    notification_id: int,
    current_user: dict = Depends(
        require_roles("ADMIN", "DOCTOR", "CAREGIVER")
    )
):
    db = SessionLocal()

    try:
        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id
            )
            .first()
        )

        if not notification:
            raise HTTPException(
                status_code=404,
                detail="Notification not found"
            )

        notification.status = "ACKNOWLEDGED"

        notification.acknowledged_at = (
            datetime.now(timezone.utc)
        )

        db.commit()
        db.refresh(notification)

        return {
            "success": True,
            "message": "Notification acknowledged",
            "notification_id": notification.id,
            "status": notification.status,
            "acknowledged_at": (
                notification.acknowledged_at.isoformat()
            )
        }

    finally:
        db.close()