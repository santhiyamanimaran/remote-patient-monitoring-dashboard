
import { useState, useEffect, useCallback } from "react";
import api from "./services/api";
import "./App.css";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function App() {
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activePage, setActivePage] = useState("Dashboard");
  const [patientId, setPatientId] = useState("1");
  const [showPatientForm, setShowPatientForm] = useState(false);
const [patientName, setPatientName] = useState("");
const [patientAge, setPatientAge] = useState("");
const [patientGender, setPatientGender] = useState("");
const [patientMessage, setPatientMessage] = useState("");
const [savingPatient, setSavingPatient] = useState(false);

  const [data, setData] = useState({
    patients: [],
    vitals: [],
    alerts: [],
    notifications: [],
    contacts: [],
  });

  const loadData = useCallback(async () => {
    if (!token) return;

    const endpoints = [
      "/api/patients/",
      `/vitals/${patientId}`,
      `/alerts/${patientId}`,
      `/notifications/${patientId}`,
      `/contacts/${patientId}`,
    ];

    const results = await Promise.allSettled(
      endpoints.map((url) => api.get(url))
    );

    const getRows = (index) => {
      if (results[index].status !== "fulfilled") return [];

      const result = results[index].value.data;

      if (Array.isArray(result)) return result;

      return result?.items || result?.results || [];
    };

    const patients = getRows(0);

    setData({
      patients,
      vitals: getRows(1),
      alerts: getRows(2),
      notifications: getRows(3),
      contacts: getRows(4),
    });

    if (
      patients.length &&
      !patients.some(
        (p) => String(p.id) === String(patientId)
      )
    ) {
      setPatientId(String(patients[0].id));
    }
  }, [token, patientId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError("");
    setLoading(true);

    try {
      // Backend endpoint: POST /auth/login
      const response = await api.post("/auth/login", {
        username,
        password,
      });

      const accessToken = response.data.access_token;

      if (!accessToken) {
        throw new Error("Access token was not returned by the server.");
      }

      localStorage.setItem("access_token", accessToken);
      setToken(accessToken);
      setPassword("");
    } catch (error) {
      setLoginError(
        error.response?.data?.detail ||
          error.message ||
          "Login failed. Check your username and password."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUsername("");
    setPassword("");
    setLoginError("");
    setActivePage("Dashboard");
  };
const handleAddPatient = async (e) => {
  e.preventDefault();
  setPatientMessage("");
  setSavingPatient(true);

  try {
    await api.post("/api/patients/", {
      name: patientName.trim(),
      age: Number(patientAge),
      gender: patientGender,
    });

    setPatientMessage("Patient added successfully!");
    setPatientName("");
    setPatientAge("");
    setPatientGender("");
    setShowPatientForm(false);

    await loadData();
  } catch (error) {
    setPatientMessage(
      error.response?.data?.detail ||
        "Unable to add patient. Please check the details."
    );
  } finally {
    setSavingPatient(false);
  }
};
  const formatDate = (value) => {
    if (!value) return "-";

    const date = new Date(value);

    return Number.isNaN(date.getTime())
      ? value
      : date.toLocaleString();
  };

  const getVitalStatus = (value, min, max) => {
    if (
      value === null ||
      value === undefined ||
      value === ""
    ) {
      return "No Data";
    }

    const number = Number(value);

    if (!Number.isFinite(number)) return "No Data";

    return number >= min && number <= max
      ? "Normal"
      : "Check";
  };

  const latestVital = data.vitals[0] || {};

  const chartData = [...data.vitals]
    .reverse()
    .map((vital, index) => ({
      ...vital,
      chartTime: vital.recorded_at
        ? new Date(vital.recorded_at).toLocaleTimeString(
            [],
            {
              hour: "2-digit",
              minute: "2-digit",
            }
          )
        : `Reading ${index + 1}`,
      heart_rate:
        vital.heart_rate == null
          ? null
          : Number(vital.heart_rate),
      spo2:
        vital.spo2 == null ? null : Number(vital.spo2),
    }))
    .filter(
      (vital) =>
        Number.isFinite(vital.heart_rate) ||
        Number.isFinite(vital.spo2)
    );

  const menuItems = [
    "Dashboard",
    "Patients",
    "Vital Readings",
    "Alerts",
    "Notifications",
    "Emergency Contacts",
  ];

  const StatCard = ({ title, value, unit, icon }) => {
    const colors = {
      "Total Patients": "#3182f6",
      "Heart Rate": "#e84d6a",
      "Blood Oxygen": "#0d9f83",
      Temperature: "#f59e0b",
      Alerts: "#8b5cf6",
      Notifications: "#0891b2",
    };

    const color = colors[title] || "#3182f6";

    return (
      <div className="stat-card">
        <div className="stat-card-top">
          <span className="stat-title">
            <span
              className="stat-icon-circle"
              style={{
                color,
                backgroundColor: `${color}20`,
              }}
            >
              {icon}
            </span>
            {title}
          </span>
        </div>

        <h2>
          {value ?? "--"} <small>{unit}</small>
        </h2>
      </div>
    );
  };

  const StatusCard = ({
    title,
    value,
    unit,
    min,
    max,
    icon,
  }) => {
    const status = getVitalStatus(value, min, max);

    return (
      <div className="status-card">
        <h3>
          {icon} {title}
        </h3>

        <p>
          {value ?? "--"} {unit}
        </p>

        <span
          className={
            status === "Normal"
              ? "vital-normal"
              : status === "Check"
              ? "vital-check"
              : "vital-no-data"
          }
        >
          {status}
        </span>
      </div>
    );
  };

  const Table = ({ columns, rows, emptyMessage }) => (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>{column.label}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.length ? (
            rows.map((row, index) => (
              <tr key={row.id ?? index}>
                {columns.map((column) => (
                  <td key={column.key}>
                    {column.render
                      ? column.render(row[column.key], row)
                      : row[column.key] ?? "-"}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length}
                className="empty-message"
              >
                {emptyMessage || "No records found"}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );

  if (!token) {
    return (
      <div className="login-page">
        <div className="login-card">
          <div className="login-logo">🏥</div>

          <h1>HealthTrack</h1>

          <p className="login-subtitle">
            Remote Patient Monitoring Dashboard
          </p>

          <form onSubmit={handleLogin}>
            <label>Username</label>

            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              autoComplete="username"
              required
            />

            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              autoComplete="current-password"
              required
            />

            {loginError && (
              <p className="error-message">{loginError}</p>
            )}

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">➕</div>

          <div>
            <h2>HealthTrack</h2>
            <p>Patient Monitoring</p>
          </div>
        </div>

        <p className="menu-heading">MAIN MENU</p>

        <nav>
          {menuItems.map((item) => (
            <button
              key={item}
              className={`nav-item ${
                activePage === item ? "active" : ""
              }`}
              onClick={() => setActivePage(item)}
            >
              <span>
                {item === "Dashboard" && "▦"}
                {item === "Patients" && "♙"}
                {item === "Vital Readings" && "♥"}
                {item === "Alerts" && "⚠"}
                {item === "Notifications" && "♧"}
                {item === "Emergency Contacts" && "☎"}
              </span>

              {item}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="online-indicator">
            <span /> System Online
          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            ⇥ Logout
          </button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h2>{activePage}</h2>
            <p>Remote Patient Monitoring System</p>
          </div>

          <div className="topbar-right">
            <span className="status-badge">● Online</span>

            <button
              className="refresh-button"
              onClick={loadData}
            >
              ↻ Refresh
            </button>
          </div>
        </header>

        {data.patients.length > 0 && (
          <div className="patient-selector">
            <label htmlFor="patient">
              Select Patient:
            </label>

            <select
              id="patient"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
            >
              {data.patients.map((patient) => (
                <option
                  key={patient.id}
                  value={patient.id}
                >
                  {patient.name ||
                    patient.full_name ||
                    `Patient ${patient.id}`}
                </option>
              ))}
            </select>
          </div>
        )}

        {activePage === "Dashboard" && (
          <>
            <section className="welcome">
              <div>
                <h1>Welcome to HealthTrack 👋</h1>
                <p>
                  Monitor patient health and vital readings
                  in one place.
                </p>
              </div>

              <div className="welcome-heart">♥</div>
            </section>

            <section className="stats-grid">
              <StatCard
                title="Total Patients"
                value={data.patients.length}
                icon="♙"
              />

              <StatCard
                title="Heart Rate"
                value={latestVital.heart_rate}
                unit="BPM"
                icon="♥"
              />

              <StatCard
                title="Blood Oxygen"
                value={latestVital.spo2}
                unit="%"
                icon="◉"
              />

              <StatCard
                title="Temperature"
                value={latestVital.temperature}
                unit="°C"
                icon="♨"
              />

              <StatCard
                title="Alerts"
                value={data.alerts.length}
                icon="⚠"
              />

              <StatCard
                title="Notifications"
                value={data.notifications.length}
                icon="♧"
              />
            </section>

            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Vital Status</h2>
                  <p>Overview of the latest readings</p>
                </div>
              </div>

              <div className="status-grid">
                <StatusCard
                  title="Heart Rate"
                  value={latestVital.heart_rate}
                  unit="BPM"
                  min={60}
                  max={100}
                  icon="❤️"
                />

                <StatusCard
                  title="SpO₂"
                  value={latestVital.spo2}
                  unit="%"
                  min={95}
                  max={100}
                  icon="🫁"
                />

                <StatusCard
                  title="Temperature"
                  value={latestVital.temperature}
                  unit="°C"
                  min={36.1}
                  max={37.5}
                  icon="🌡️"
                />
              </div>

              <p className="status-note">
                Demo ranges only. These labels are not a
                medical diagnosis.
              </p>
            </section>

            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Vital Readings Chart</h2>
                  <p>
                    Heart rate and blood oxygen over time
                  </p>
                </div>
              </div>

              {chartData.length > 0 ? (
                <ResponsiveContainer
                  width="100%"
                  height={320}
                >
                  <LineChart
                    data={chartData}
                    margin={{
                      top: 10,
                      right: 20,
                      left: 0,
                      bottom: 10,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="chartTime" />
                    <YAxis />
                    <Tooltip />
                    <Legend />

                    <Line
                      type="monotone"
                      dataKey="heart_rate"
                      name="Heart Rate (BPM)"
                      stroke="#e84d6a"
                      strokeWidth={2}
                      connectNulls
                    />

                    <Line
                      type="monotone"
                      dataKey="spo2"
                      name="SpO₂ (%)"
                      stroke="#0d9f83"
                      strokeWidth={2}
                      connectNulls
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <p className="empty-message">
                  No vital readings available for the chart.
                </p>
              )}
            </section>

            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h2>Recent Vital Readings</h2>
                  <p>
                    Latest patient health measurements
                  </p>
                </div>
              </div>

              <Table
                columns={[
                  {
                    key: "recorded_at",
                    label: "Date & Time",
                    render: formatDate,
                  },
                  {
                    key: "heart_rate",
                    label: "Heart Rate (BPM)",
                  },
                  {
                    key: "spo2",
                    label: "SpO₂ (%)",
                  },
                  {
                    key: "temperature",
                    label: "Temperature (°C)",
                  },
                ]}
                rows={data.vitals.slice(0, 10)}
                emptyMessage="No vital readings found"
              />
            </section>
          </>
        )}

       {activePage === "Patients" && (
  <section className="panel">
    <div className="panel-heading">
      <div>
        <h2>Patients</h2>
        <p>Registered patients</p>
      </div>

      <button
        className="primary-button"
        type="button"
        onClick={() => {
          setPatientMessage("");
          setShowPatientForm(!showPatientForm);
        }}
      >
        {showPatientForm ? "Cancel" : "+ Add Patient"}
      </button>
    </div>

    {patientMessage && (
      <p className="status-note">{patientMessage}</p>
    )}

    {showPatientForm && (
      <form
        onSubmit={handleAddPatient}
        className="patient-form"
      >
        <h3>Add New Patient</h3>

        <label htmlFor="patientName">Patient Name</label>
        <input
          id="patientName"
          type="text"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
          placeholder="Enter patient name"
          required
        />

        <label htmlFor="patientAge">Age</label>
        <input
          id="patientAge"
          type="number"
          min="1"
          max="120"
          value={patientAge}
          onChange={(e) => setPatientAge(e.target.value)}
          placeholder="Enter age"
          required
        />

        <label htmlFor="patientGender">Gender</label>
        <select
          id="patientGender"
          value={patientGender}
          onChange={(e) => setPatientGender(e.target.value)}
          required
        >
          <option value="">Select gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>

        <button
          className="primary-button"
          type="submit"
          disabled={savingPatient}
        >
          {savingPatient ? "Saving..." : "Save Patient"}
        </button>
      </form>
    )}

    <Table
      columns={[
        { key: "id", label: "ID" },
        { key: "name", label: "Name" },
        { key: "age", label: "Age" },
        { key: "gender", label: "Gender" },
      ]}
      rows={data.patients}
    />
  </section>
)}

        {activePage === "Vital Readings" && (
          <section className="panel">
            <h2>Vital Readings</h2>

            <Table
              columns={[
                {
                  key: "recorded_at",
                  label: "Date & Time",
                  render: formatDate,
                },
                {
                  key: "heart_rate",
                  label: "Heart Rate (BPM)",
                },
                { key: "spo2", label: "SpO₂ (%)" },
                {
                  key: "temperature",
                  label: "Temperature (°C)",
                },
              ]}
              rows={data.vitals}
            />
          </section>
        )}

        {activePage === "Alerts" && (
          <section className="panel">
            <h2>Alerts</h2>

            <Table
              columns={[
                { key: "id", label: "ID" },
                { key: "message", label: "Message" },
                { key: "severity", label: "Severity" },
                { key: "status", label: "Status" },
                {
                  key: "created_at",
                  label: "Date",
                  render: formatDate,
                },
              ]}
              rows={data.alerts}
            />
          </section>
        )}

        {activePage === "Notifications" && (
          <section className="panel">
            <h2>Notifications</h2>

            <Table
              columns={[
                { key: "id", label: "ID" },
                { key: "message", label: "Message" },
                { key: "type", label: "Type" },
                { key: "status", label: "Status" },
                {
                  key: "created_at",
                  label: "Date",
                  render: formatDate,
                },
              ]}
              rows={data.notifications}
            />
          </section>
        )}

        {activePage === "Emergency Contacts" && (
          <section className="panel">
            <h2>Emergency Contacts</h2>

            <Table
              columns={[
                { key: "id", label: "ID" },
                { key: "name", label: "Name" },
                {
                  key: "relationship",
                  label: "Relationship",
                },
                { key: "phone", label: "Phone" },
              ]}
              rows={data.contacts}
            />
          </section>
        )}

        <footer className="footer">
          Remote Patient Monitoring Dashboard
        </footer>
      </main>
    </div>
  );
}

export default App;
