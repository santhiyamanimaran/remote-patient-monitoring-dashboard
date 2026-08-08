# System Architecture
## 1. Project Overview
The Remote Patient Monitoring Dashboard is a web-based system used to monitor
patient health data remotely.
The system collects health readings such as heart rate, SpO2, temperature,
and steps. The data is sent to the backend, stored in the database, and
displayed on the dashboard.
## 2. Technology Stack
### Frontend
- React.js
- JavaScript
- Bootstrap
- CSS
### Backend
- Python
- FastAPI
### Database
- MySQL
- SQLAlchemy ORM
### Authentication
- JWT Authentication
### Testing
- Pytest
### AI Enhancement
- AI-based health data anomaly detection
## 3. Architecture Flow
Patient / Simulated Wearable Data
        ↓
React Frontend
        ↓
FastAPI REST API
        ↓
Business Logic
        ↓
AI Anomaly Detection
        ↓
SQLAlchemy ORM
        ↓
MySQL Database
        ↓
React Dashboard
        ↓
Doctor / Patient / Family Member
## 4. Main Components
### Frontend
Provides login pages, patient dashboard, doctor dashboard,
family member dashboard, health charts, and alerts.
### Backend
Handles authentication, health data ingestion, patient management,
alert generation, and REST API requests.
### Database
Stores users, patients, family members, devices, health readings,
and alerts.
### Business Logic
Checks health readings and creates alerts when readings meet
the configured monitoring conditions.
### AI Component
Analyzes health readings and identifies unusual patterns.
The AI feature is used only as a monitoring aid and does not provide
medical diagnosis.
## 5. User Roles
### Doctor
- View assigned patients
- View health readings
- View health history
- View alerts
### Patient
- View own health readings
- View health history
- View device information
### Family Member
- View authorized patient information
- View health readings
- View alerts