from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.core.database import Base


class VitalReading(Base):
    __tablename__ = "vital_readings"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    heart_rate = Column(Float, nullable=False)
    spo2 = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    systolic_bp = Column(Float, nullable=False)
    diastolic_bp = Column(Float, nullable=False)
    sugar_level = Column(Float, nullable=False)

    # Data source
    source = Column(
        String,
        nullable=False,
        default="WEARABLE_DEVICE"
    )

    recorded_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )