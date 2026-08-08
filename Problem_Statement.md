# Problem Statement
## 1. Title
Remote Patient Monitoring Dashboard Using Wearable Data
## 2. Domain
HealthTech
## 3. Who is the user?
1. Doctor
2. Patient
3. Family Member
## 4. What problem are we solving?
Patients who need continuous health monitoring may require their health information
to be monitored regularly. Doctors and family members may not always be able to
check the patient's health readings manually. The system provides a centralized
dashboard to monitor wearable health data such as heart rate, SpO2, temperature,
and steps. It also identifies abnormal readings and generates alerts for monitoring.
## 5. Proposed Solution
The proposed system is a web-based remote patient monitoring application.
Patients' wearable health data will be collected and stored in the database.
Doctors and authorized family members can view the patient's latest readings,
historical health data, and alerts through a dashboard. The system will provide
role-based access, health-data monitoring, abnormal-reading detection, and
dashboard updates.
## 6. Core Entities / Database Tables
1. Users
2. Patients
3. Family Members
4. Devices
5. Health Readings
6. Alerts
## 7. User Roles & Permissions
### Doctor
- Login securely
- View assigned patients
- View health readings
- View health history
- View alerts
### Patient
- Login securely
- View own health readings
- View health history
- View connected device
### Family Member
- Login securely
- View authorized patient's health readings
- View health history
- View alerts
## 8. Success Criteria
- Users should be able to securely log in based on their role.
- Doctors should be able to view assigned patient health data.
- Patients should be able to view their own health readings.
- The system should store health readings correctly.
- Abnormal readings should generate alerts.
- The dashboard should display recent health information clearly.
## 9. Out of Scope
- Real medical diagnosis
- Prescription generation
- Direct control of medical devices
- Emergency medical decision-making
- Real wearable hardware integration in the initial version
## 10. Chosen Track
Python - FastAPI