from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    alert_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    contact_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    message = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    sent_at = Column(
        DateTime,
        nullable=True
    )

    acknowledged_at = Column(
        DateTime,
        nullable=True
    )