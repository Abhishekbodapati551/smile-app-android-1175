# Live GitHub Pages E2E Execution Summary

**Deployment URL:**
[file:///C:/Users/bodap/AndroidStudioProjects/smileapp/index.html/](file:///C:/Users/bodap/AndroidStudioProjects/smileapp/index.html/)

**Execution Date:**
2026-07-25 11:31:54 UTC

**Build Status:**
`PASS`

**Deployment Status:**
`PASS`

**Total Test Cases:**
`470`

| Metric | Value |
| --- | --- |
| **Executed** | 470 |
| **Passed** | 300 |
| **Failed** | 170 |
| **Skipped** | 0 |
| **Pass Percentage** | **63.83%** |
| **Execution Duration** | 3213.62s |

---

### Top Passing Modules

| Module Name | Pass Rate | Passed / Total |
| --- | --- | --- |
| **Accessibility** | 100.0% | 20 / 20 |
| **Authorization** | 100.0% | 40 / 40 |
| **CRUD Operations** | 100.0% | 50 / 50 |
| **Error Handling** | 100.0% | 20 / 20 |
| **File Upload** | 100.0% | 20 / 20 |
| **Input Validation** | 100.0% | 40 / 40 |
| **Performance Smoke Tests** | 100.0% | 20 / 20 |
| **Regression** | 100.0% | 50 / 50 |
| **Responsive Design** | 100.0% | 20 / 20 |
| **Session Management** | 100.0% | 20 / 20 |

---

### Failed Tests

| Test ID | Test Name | Failure Reason |
| --- | --- | --- |
| `TC_AUTH_001` | test_auth_cases[1] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_002` | test_auth_cases[2] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_003` | test_auth_cases[3] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_004` | test_auth_cases[4] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_005` | test_auth_cases[5] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_006` | test_auth_cases[6] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_007` | test_auth_cases[7] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_008` | test_auth_cases[8] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_009` | test_auth_cases[9] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_010` | test_auth_cases[10] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_011` | test_auth_cases[11] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_012` | test_auth_cases[12] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_013` | test_auth_cases[13] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |
| `TC_AUTH_014` | test_auth_cases[14] | automation\tests\test_authentication.py:31: in test_auth_cases
    start_page.click_doctor_login()
automation\pages\start_page.py:17: in click_doctor_login
    self.js_click(*self.DOCTOR_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^^^^ |
| `TC_AUTH_015` | test_auth_cases[15] | automation\tests\test_authentication.py:22: in test_auth_cases
    start_page.click_patient_login()
automation\pages\start_page.py:14: in click_patient_login
    self.js_click(*self.PATIENT_BTN)
automation\pages\base_page.py:35: in js_click
    element = self.find_element(by, value)
              ^^ |

---

### Artifacts Generated

- ✓ Excel Reports (`Automation_Test_Report.xlsx`, `Failed_Test_Cases.xlsx`, `Passed_Test_Cases.xlsx`, `Summary_Report.xlsx`)
- ✓ HTML Reports (`execution-report.html`, `dashboard.html`)
- ✓ Failure Screenshots & Browser Logs
- ✓ JSON Results (`execution-results.json`)
- ✓ Complete ZIP Bundle (`smileapp-e2e-automation.zip`)
