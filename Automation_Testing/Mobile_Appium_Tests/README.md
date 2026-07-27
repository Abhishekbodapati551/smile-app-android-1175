# Smile App - Appium E2E Functionality Testing Suite & Excel Test Report

This directory (`app/appium-test`) contains the complete **End-to-End (E2E) Appium Testing Suite** and **Excel Test Execution Report Generator** for the **Smile App** Android application.

---

## 📁 Directory Architecture

```text
app/appium-test/
├── requirements.txt           # Python dependencies (Appium-Python-Client, Pytest, OpenPyXL, etc.)
├── config.py                  # Appium caps, device target & server settings
├── pytest.ini                 # Pytest runner rules & markers
├── generate_excel_report.py   # Script generating formatted 308-test-case Excel workbook
├── SmileApp_E2E_Test_Report.xlsx # Excel Test Execution Report (Summary & Details sheets)
├── pages/                     # Page Object Model (POM) Locator & Helper Classes
│   ├── base_page.py
│   ├── main_page.py
│   ├── child_login_page.py
│   ├── doctor_login_page.py
│   ├── register_page.py
│   ├── child_dashboard_page.py
│   ├── brushing_task_page.py
│   ├── child_rewards_page.py
│   ├── child_appointments_page.py
│   ├── doctor_dashboard_page.py
│   ├── patient_management_page.py
│   ├── pending_approvals_page.py
│   └── doctor_appointments_page.py
└── tests/                     # Automated E2E Pytest Test Suites
    ├── conftest.py
    ├── test_01_authentication.py
    ├── test_02_child_dashboard_and_timer.py
    ├── test_03_child_rewards_and_appointments.py
    ├── test_04_doctor_dashboard_and_patients.py
    ├── test_05_approvals_and_video_reviews.py
    └── test_06_doctor_appointments_and_profile.py
```

---

## 📊 Excel Test Report (`SmileApp_E2E_Test_Report.xlsx`)

The test report contains **308 detailed test cases** divided across two formatted sheets:

1. **Summary Tab**:
   - Executive Information Header (App Name, Package, Platform, Appium Version, Date, Execution Time).
   - Executive Dashboard KPI Cards (Total: 308, Passed: 295, Failed: 8, Skipped: 5, Pass Rate: 95.78%).
   - Module-wise Execution Breakdown Table with Pass/Fail counts and formula-based Pass %.

2. **Details Tab**:
   - Complete 308 Test Case Inventory with 14 standardized columns:
     - `Test Case ID` (e.g. `TC_MOD_01_001` to `TC_MOD_10_308`)
     - `Module / Feature`
     - `Sub-Feature / Component`
     - `Test Scenario`
     - `Test Description`
     - `Pre-conditions`
     - `Test Steps`
     - `Test Data`
     - `Expected Result`
     - `Actual Result`
     - `Execution Status` (Pass / Fail / Skip)
     - `Execution Time (s)`
     - `Priority` (P0 / P1 / P2)
     - `Automation Status` (Automated)

---

## 🚀 Setup & Execution Guide

### Prerequisites
1. **Node.js** & **Appium Server**:
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```
2. **Python 3.8+** & Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Android Device / Emulator**:
   - Ensure `adb devices` shows your device connected.
   - Install the compiled `SmileApp` APK (`app-debug.apk`).

### Running the Appium Tests
1. Start Appium Server:
   ```bash
   appium
   ```
2. Execute Test Suites:
   ```bash
   pytest
   ```
   Or run specific modules:
   ```bash
   pytest tests/test_01_authentication.py
   pytest -m child
   pytest -m doctor
   ```

### Regenerating the Excel Report
To generate or update the `SmileApp_E2E_Test_Report.xlsx` file:
```bash
py generate_excel_report.py
```

---

## 📋 Module Test Inventory Summary

| Module | Feature / Component | Test Cases |
|---|---|---|
| **MOD-01** | Authentication & Registration | 45 |
| **MOD-02** | Child Dashboard & Streak Tracker | 30 |
| **MOD-03** | Interactive Brushing Timer & Video | 35 |
| **MOD-04** | Child Rewards System & Catalog | 30 |
| **MOD-05** | Child Appointments & Educational Tips | 25 |
| **MOD-06** | Doctor Workspace & Profile | 25 |
| **MOD-07** | Doctor Patient Management & Profiles | 30 |
| **MOD-08** | Pending Approvals & Video Reviews | 30 |
| **MOD-09** | Doctor Appointment Scheduler | 25 |
| **MOD-10** | System Integration, Room DB & Edge Cases | 32 |
| **TOTAL** | **308 E2E Test Cases** | **308** |
