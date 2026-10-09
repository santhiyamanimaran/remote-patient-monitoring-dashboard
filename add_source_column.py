import sqlite3
db = sqlite3.connect("remote_patient_monitoring.db")
db.execute("""
    ALTER TABLE vital_readings
    ADD COLUMN source VARCHAR NOT NULL
    DEFAULT 'WEARABLE_DEVICE'
""")
db.commit()
db.close()
print("Vital source migration completed successfully")