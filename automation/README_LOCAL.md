# Local Execution Guide - SmileApp Selenium E2E Automation

## Prerequisites
1. Python 3.10+ installed.
2. Google Chrome installed.
3. ChromeDriver (managed automatically by Selenium WebDriver 4.x or Chrome system driver).

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r automation/requirements.txt
```

### 2. Configure Environment (Optional)
By default, tests execute against the live GitHub Pages URL or configured `BASE_URL`.
```bash
# Windows PowerShell
$env:BASE_URL="https://abhishekbodapati551.github.io/smile-app-android-1175/"
$env:HEADLESS="true"

# Bash / Linux / macOS
export BASE_URL="https://abhishekbodapati551.github.io/smile-app-android-1175/"
export HEADLESS="true"
```

### 3. Run Test Suite
```bash
python automation/run_tests.py
```

### 4. Generated Artifacts
After execution completes, check:
- Excel Reports: `automation/reports/Excel/`
  - `Automation_Test_Report.xlsx`
  - `Failed_Test_Cases.xlsx`
  - `Passed_Test_Cases.xlsx`
  - `Summary_Report.xlsx`
- HTML Reports: `automation/reports/HTML/`
  - `execution-report.html`
  - `dashboard.html`
- JSON Results: `automation/reports/JSON/execution-results.json`
- Step Summary: `automation/reports/Summary/summary.md`
- Downloadable Zip: `smileapp-e2e-automation.zip`
