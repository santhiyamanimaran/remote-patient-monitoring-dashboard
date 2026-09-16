from app.core.database import SessionLocal
from app.models.audit_log import AuditLog
def create_audit_log(
    user_id: int,
    action: str,
    resource: str,
    patient_id: int | None = None
):
    db = SessionLocal()
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            patient_id=patient_id
        )
        db.add(log)
        db.commit()
    finally:
        db.close()