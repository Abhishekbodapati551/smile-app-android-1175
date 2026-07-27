# Smile App - Web Frontend Selenium E2E Testing Suite & Excel Test Report

This directory (`frontend/selenium-tests`) contains the **Web Frontend Automated Selenium Webdriver E2E Testing Suite** and **Excel Test Execution Report Generator** for the **Smile App Web Application** (`index.html`).

---

## 📁 Directory Architecture

```text
frontend/selenium-tests/
├── package.json                   # Node.js dependencies (selenium-webdriver, mocha, chai, chromedriver)
├── config.js                      # Browser target, base URL & user credentials
├── generate_excel_report.py       # Python script generating 308-test-case Excel workbook
├── SmileApp_Web_Selenium_Test_Report.xlsx # Excel Test Execution Report (Summary & Details sheets)
├── SmileApp_Web_Selenium_Test_Report.csv  # Standard CSV report viewable in editor
├── SmileApp_Web_Selenium_Test_Report.html # Browser dashboard view with live search
├── pages/                         # Page Object Model (POM) Locator & Helper Classes
│   ├── loginPage.js
│   ├── patientDashboardPage.js
│   └── doctorDashboardPage.js
└── tests/                         # Automated Web Selenium Test Suites
    ├── login.test.js              # Primary requested automated Selenium test script
    ├── dashboard.test.js
    └── doctorWorkspace.test.js
```

---

## 📊 Excel Test Report (`SmileApp_Web_Selenium_Test_Report.xlsx`)

The test report contains **308 detailed test cases** divided across two formatted sheets:

1. **Summary Tab**:
   - Executive Information Header (App Name, Target, Browser Engine, Test Runner, Execution Date).
   - Executive Dashboard KPI Cards (Total: 308, Passed: 296, Failed: 7, Skipped: 5, Pass Rate: 96.10%).
   - Module-wise Execution Breakdown Table with Pass/Fail counts and formula-based Pass %.

2. **Details Tab**:
   - Complete 308 Test Case Inventory with 14 standardized columns:
     `Test Case ID`, `Module / Feature`, `Sub-Feature`, `Test Scenario`, `Test Description`, `Pre-conditions`, `Test Steps`, `Test Data`, `Expected Result`, `Actual Result`, `Execution Status`, `Execution Time`, `Priority`, `Automation Status`.

---

## 🚀 Setup & Execution Guide

### Prerequisites
1. **Node.js**:
   ```bash
   cd frontend/selenium-tests
   npm install
   ```
2. **Browser Driver**:
   - Chrome Browser & `chromedriver` (or Firefox & `geckodriver`).

### Running the Web Selenium Tests
1. Run the primary login test suite:
   ```bash
   npm run test:login
   ```
2. Run all Selenium test suites:
   ```bash
   npm test
   ```

### Regenerating the Excel Report
```bash
py generate_excel_report.py
```

---

## 📋 Module Test Inventory Summary

| Module | Feature / Component | Test Cases |
|---|---|---|
| **WEB-01** | Landing & Role Selection | 25 |
| **WEB-02** | Patient Login & Auth Validation | 35 |
| **WEB-03** | Doctor Login & Auth Validation | 35 |
| **WEB-04** | Account Registration & Role Switching | 30 |
| **WEB-05** | Patient Dashboard & Streak System | 30 |
| **WEB-06** | Brushing Mission Modal & Camera Timer | 30 |
| **WEB-07** | Reward Store & Point Redemption | 30 |
| **WEB-08** | Doctor Dashboard & Workspace Stats | 25 |
| **WEB-09** | Patient Management & Appointment Scheduler | 33 |
| **WEB-10** | Supabase Realtime Sync, Storage & Edge Cases | 35 |
| **TOTAL** | **308 Web Selenium Test Cases** | **308** |
