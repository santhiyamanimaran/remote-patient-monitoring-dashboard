from flask import Flask, render_template
from database.db import get_connection
app = Flask(__name__)
@app.route("/")
def home():
    connection = get_connection()
    reading = connection.execute("""
        SELECT heart_rate, spo2, temperature, steps
        FROM health_readings
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()
    connection.close()
    health_data = {
        "heart_rate": reading["heart_rate"],
        "spo2": reading["spo2"],
        "temperature": reading["temperature"],
        "steps": reading["steps"]
    }
    return render_template("index.html", health_data=health_data)
@app.route("/api/health")
def health_api():
    connection = get_connection()
    reading = connection.execute("""
        SELECT heart_rate, spo2, temperature, steps, recorded_at
        FROM health_readings
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()
    connection.close()
    return {
        "heart_rate": reading["heart_rate"],
        "spo2": reading["spo2"],
        "temperature": reading["temperature"],
        "steps": reading["steps"],
        "recorded_at": reading["recorded_at"]
    }
if __name__ == "__main__":
    app.run(debug=True)