from app.core.database import SessionLocal
from app.models.vital import VitalReading
from app.models.alert import Alert
from app.models.contact import EmergencyContact
from app.models.notification import Notification


def check_abnormal_vitals(data):
    alerts = []

    if data.spo2 < 90:
        alerts.append(
            ("LOW_SPO2", "SpO2 is below the demo safety limit", "HIGH")
        )

    if data.heart_rate < 50 or data.heart_rate > 120:
        alerts.append(
            ("HEART_RATE", "Heart rate is outside the demo range", "HIGH")
        )

    if data.temperature < 35 or data.temperature > 39:
        alerts.append(
            ("TEMPERATURE", "Temperature is outside the demo range", "HIGH")
        )

    if data.systolic_bp < 90 or data.systolic_bp > 180:
        alerts.append(
            (
                "BLOOD_PRESSURE",
                "Systolic blood pressure is outside the demo range",
                "HIGH",
            )
        )

    if data.diastolic_bp < 60 or data.diastolic_bp > 120:
        alerts.append(
            (
                "BLOOD_PRESSURE",
                "Diastolic blood pressure is outside the demo range",
                "HIGH",
            )
        )

    if data.sugar_level < 70 or data.sugar_level > 300:
        alerts.append(
            (
                "SUGAR_LEVEL",
                "Sugar level is outside the demo range",
                "HIGH",
            )
        )

    return alerts


def save_vital_reading(data):
    db = SessionLocal()

    try:
        reading = VitalReading(
            patient_id=data.patient_id,
            heart_rate=data.heart_rate,
            spo2=data.spo2,
            temperature=data.temperature,
            systolic_bp=data.systolic_bp,
            diastolic_bp=data.diastolic_bp,
            sugar_level=data.sugar_level,
            source="WEARABLE_DEVICE",
        )

        db.add(reading)
        db.flush()

        detected_alerts = check_abnormal_vitals(data)

        notifications_created = 0

        for alert_type, message, severity in detected_alerts:

            alert = Alert(
                patient_id=data.patient_id,
                alert_type=alert_type,
                message=message,
                severity=severity,
            )

            db.add(alert)
            db.flush()

            family_contacts = (
                db.query(EmergencyContact)
                .filter(
                    EmergencyContact.patient_id == data.patient_id,
                    EmergencyContact.contact_type == "FAMILY",
                )
                .all()
            )

            for contact in family_contacts:

                notification = Notification(
                    patient_id=data.patient_id,
                    alert_id=alert.id,
                    contact_id=contact.id,
                    message=message,
                    status="PENDING",
                )

                db.add(notification)
                notifications_created += 1

        db.commit()
        db.refresh(reading)

        return {
            "id": reading.id,
            "patient_id": reading.patient_id,
            "heart_rate": reading.heart_rate,
            "spo2": reading.spo2,
            "temperature": reading.temperature,
            "systolic_bp": reading.systolic_bp,
            "diastolic_bp": reading.diastolic_bp,
            "sugar_level": reading.sugar_level,
            "source": reading.source,
            "recorded_at": reading.recorded_at.isoformat(),
            "alerts_created": len(detected_alerts),
            "notifications_created": notifications_created,
        }

    finally:
        db.close()


def get_patient_vitals(patient_id):
    db = SessionLocal()

    try:
        readings = (
            db.query(VitalReading)
            .filter(VitalReading.patient_id == patient_id)
            .order_by(VitalReading.recorded_at.desc())
            .all()
        )

        return [
            {
                "id": reading.id,
                "patient_id": reading.patient_id,
                "heart_rate": reading.heart_rate,
                "spo2": reading.spo2,
                "temperature": reading.temperature,
                "systolic_bp": reading.systolic_bp,
                "diastolic_bp": reading.diastolic_bp,
                "sugar_level": reading.sugar_level,
                "source": reading.source,
                "recorded_at": reading.recorded_at.isoformat(),
            }
            for reading in readings
        ]

    finally:
        db.close()