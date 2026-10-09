# Database Design

## 1. Database

Database: MySQL

ORM: SQLAlchemy

The system uses six related tables to store user information,
patient details, wearable devices, health readings, and alerts.

---

## 2. Users Table

Stores login details and user roles.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| name | VARCHAR(100) | |
| email | VARCHAR(150) | Unique |
| password | VARCHAR(255) | |
| role | VARCHAR(30) | |
| created_at | DATETIME | |

Roles:
- Doctor
- Patient
- Family Member

---

## 3. Patients Table

Stores patient information.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| user_id | INT | Foreign Key |
| date_of_birth | DATE | |
| gender | VARCHAR(20) | |
| phone | VARCHAR(20) | |
| address | VARCHAR(255) | |

Relationship:

users.id → patients.user_id

---

## 4. Family Members Table

Stores family members who are authorized to monitor a patient.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| user_id | INT | Foreign Key |
| patient_id | INT | Foreign Key |
| relationship | VARCHAR(50) | |

Relationships:

users.id → family_members.user_id

patients.id → family_members.patient_id

---

## 5. Devices Table

Stores wearable or simulated device information.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| patient_id | INT | Foreign Key |
| device_name | VARCHAR(100) | |
| device_type | VARCHAR(50) | |
| device_status | VARCHAR(30) | |
| registered_at | DATETIME | |

Relationship:

patients.id → devices.patient_id

---

## 6. Health Readings Table

Stores health readings received from the wearable or simulated device.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| patient_id | INT | Foreign Key |
| device_id | INT | Foreign Key |
| heart_rate | INT | |
| spo2 | DECIMAL(5,2) | |
| temperature | DECIMAL(5,2) | |
| steps | INT | |
| recorded_at | DATETIME | |

Relationships:

patients.id → health_readings.patient_id

devices.id → health_readings.device_id

---

## 7. Alerts Table

Stores alerts generated from abnormal health readings.

| Column | Type | Key |
|---|---|---|
| id | INT | Primary Key |
| patient_id | INT | Foreign Key |
| reading_id | INT | Foreign Key |
| alert_type | VARCHAR(50) | |
| message | VARCHAR(255) | |
| status | VARCHAR(30) | |
| created_at | DATETIME | |

Relationships:

patients.id → alerts.patient_id

health_readings.id → alerts.reading_id

---

## 8. Table Relationships

users
    |
    ├── patients
    |
    └── family_members
             |
             └── patients

patients
    |
    └── devices
             |
             └── health_readings
                         |
                         └── alerts

---

## 9. Database Summary

Total Tables: 6

1. users
2. patients
3. family_members
4. devices
5. health_readings
6. alerts

The database is designed to keep patient information,
health readings, device information, and alerts organized
and related through primary and foreign keys.