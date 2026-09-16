import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [vitals, setVitals] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const patientId = 1;

  useEffect(() => {
    fetchVitals();
  }, []);

  async function fetchVitals() {
    try {
      setLoading(true);
      setError("");

      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("Please login first. JWT token not found.");
        setLoading(false);
        return;
      }

      const response = await fetch(
        `${API_URL}/vitals/${patientId}`,
        {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();

      if (data.length > 0) {
        setVitals(data[0]);
      } else {
        setError("No vital readings found.");
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load patient vitals.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>🏥 Loading Patient Dashboard...</h2>
        <p>Connecting to health monitoring server...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-page">
        <h2>⚠️ Dashboard Error</h2>
        <p>{error}</p>
        <button onClick={fetchVitals}>Retry</button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>🏥 Remote Patient Monitoring</h1>
          <p>Smart health monitoring dashboard</p>
        </div>

        <div className="status">
          <span className="dot"></span>
          System Online
        </div>
      </header>

      <section className="patient-card">
        <div>
          <h2>Patient: John</h2>
          <p>Patient ID: {patientId}</p>
        </div>

        <div className="patient-status">
          🟢 Monitoring Active
        </div>
      </section>

      <section className="vitals-grid">
        <div className="vital-card">
          <div className="icon">❤️</div>
          <h3>Heart Rate</h3>
          <div className="value">
            {vitals.heart_rate} <span>BPM</span>
          </div>
        </div>

        <div className="vital-card">
          <div className="icon">🫁</div>
          <h3>SpO₂</h3>
          <div className="value">
            {vitals.spo2} <span>%</span>
          </div>
        </div>

        <div className="vital-card">
          <div className="icon">🌡️</div>
          <h3>Temperature</h3>
          <div className="value">
            {vitals.temperature} <span>°C</span>
          </div>
        </div>

        <div className="vital-card">
          <div className="icon">🩺</div>
          <h3>Blood Pressure</h3>
          <div className="value">
            {vitals.systolic_bp}/{vitals.diastolic_bp}
            <span> mmHg</span>
          </div>
        </div>

        <div className="vital-card">
          <div className="icon">🍬</div>
          <h3>Blood Glucose</h3>
          <div className="value">
            {vitals.sugar_level} <span>mg/dL</span>
          </div>
        </div>
      </section>

      <section className="panel">
        <h2>📊 Latest Reading</h2>

        <p><strong>Reading ID:</strong> {vitals.id}</p>
        <p><strong>Patient ID:</strong> {vitals.patient_id}</p>
        <p>
          <strong>Recorded At:</strong>{" "}
          {new Date(vitals.recorded_at).toLocaleString()}
        </p>
      </section>

      <section className="panel">
        <h2>🚨 Health Alert Status</h2>

        {vitals.spo2 < 90 || vitals.heart_rate > 120 ? (
          <div className="alert warning">
            ⚠️ Abnormal vital reading detected. Doctor attention required.
          </div>
        ) : (
          <div className="alert normal-alert">
            ✅ Patient vitals are currently within monitoring range.
          </div>
        )}
      </section>

      <div className="refresh-container">
        <button className="refresh-btn" onClick={fetchVitals}>
          🔄 Refresh Vitals
        </button>
      </div>

      <footer>
        Remote Patient Monitoring System • Secure Health Dashboard
      </footer>
    </div>
  );
}

export default App;