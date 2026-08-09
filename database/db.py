import sqlite3
def get_connection():
    connection = sqlite3.connect("database/monitoring.db")
    connection.row_factory = sqlite3.Row
    return connection
def create_database():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS health_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            heart_rate INTEGER,
            spo2 INTEGER,
            temperature REAL,
            steps INTEGER,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()
def insert_reading(patient_id, heart_rate, spo2, temperature, steps):
    connection = get_connection()
    connection.execute("""
        INSERT INTO health_readings
        (patient_id, heart_rate, spo2, temperature, steps)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_id, heart_rate, spo2, temperature, steps))
    connection.commit()
    connection.close()
if __name__ == "__main__":
    create_database()
    print("Database created successfully.")