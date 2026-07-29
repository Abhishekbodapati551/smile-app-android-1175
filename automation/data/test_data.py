"""
Centralized Test Data for SmileApp Selenium E2E Automation
"""

VALID_PATIENT = {
    "email": "patient@example.com",
    "password": "Password123!",
    "name": "Alex Patient"
}

VALID_DOCTOR = {
    "email": "doctor@example.com",
    "password": "DoctorPassword123!",
    "name": "Dr. Sarah Smith",
    "doctor_id": "1234"
}

INVALID_USERS = [
    {"email": "invalid@test.com", "password": "WrongPassword", "desc": "Invalid Credentials"},
    {"email": "", "password": "Password123!", "desc": "Empty Email"},
    {"email": "patient@example.com", "password": "", "desc": "Empty Password"},
    {"email": "bademailformat", "password": "Password123!", "desc": "Bad Email Format"},
    {"email": "' OR '1'='1", "password": "' OR '1'='1", "desc": "SQL Injection Pattern"},
    {"email": "<script>alert(1)</script>", "password": "password", "desc": "XSS Script Tag"}
]

NEW_REGISTRATION_PATIENT = {
    "name": "New Test Patient",
    "email": "newpatient@test.com",
    "password": "SecurePassword123!",
    "role": "child"
}

NEW_REGISTRATION_DOCTOR = {
    "name": "Dr. New Test Doctor",
    "email": "newdoctor@test.com",
    "password": "SecurePassword123!",
    "doctor_id": "9999",
    "role": "doctor"
}

SAMPLE_APPOINTMENT = {
    "patient_name": "Test Patient",
    "date": "2026-08-01",
    "time": "10:00 AM",
    "notes": "Regular dental checkup and cleaning"
}

SAMPLE_FEEDBACK = {
    "message": "Great progress on brushing mission! Keep up the good work.",
    "rating": 5
}
