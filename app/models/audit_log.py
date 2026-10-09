from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from app.core.database import Base
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )
    action = Column(
        String,
        nullable=False
    )
    resource = Column(
        String,
        nullable=False
    )
    patient_id = Column(
        Integer,
        nullable=True,
        index=True
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )