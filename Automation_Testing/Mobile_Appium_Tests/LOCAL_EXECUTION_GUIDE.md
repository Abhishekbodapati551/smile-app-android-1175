# Local Execution Guide - Android Appium E2E Automation Framework

This guide provides step-by-step instructions to run the 400+ Appium test suite and report generators locally on your development machine.

---

## Prerequisites

1. **Java Development Kit (JDK 17 or higher)**
   - Verify: `java -version`
2. **Android SDK & Command Line Tools**
   - Ensure `ANDROID_HOME` environment variable is configured.
3. **Node.js (v18 or v20)** & **Appium**
   - Verify: `node -v` and `appium -v`
   - Install Appium UiAutomator2 driver:
     ```bash
     appium driver install uiautomator2
     ```
4. **Python (3.10+)**
   - Install dependencies:
     ```bash
     pip install -r app/appium-test/requirements.txt
     pip install openpyxl jinja2 pandas requests pytest Appium-Python-Client
     ```

---

## Local Execution Steps

### 1. Build the Android Application APK
```bash
# Windows
gradlew.bat assembleDebug

# Linux/macOS
./gradlew assembleDebug
```

### 2. Launch Android Emulator or Connect Physical Device
Verify your device is online:
```bash
adb devices
```

### 3. Start Appium Server
```bash
appium
```
Default server URL: `http://127.0.0.1:4723/`

### 4. Generate Test Cases Data & Execute Test Suite
```bash
# Navigate to repository root
py app/appium-test/generate_400_test_data.py

# Execute Pytest test suite
pytest app/appium-test/tests/ -v
```

### 5. Generate Multi-Format Enterprise Reports & Zip Package
```bash
py app/appium-test/generate_enterprise_reports.py
```

Generated reports location:
- Excel: `app/appium-test/Test Results/Excel/`
- HTML: `app/appium-test/Test Results/HTML/`
- JSON: `app/appium-test/Test Results/JSON/`
- Markdown: `app/appium-test/Test Results/Summary/summary.md`
- Downloadable Zip Artifact: `app/appium-test/Test Results/SmileApp_Android_Appium_E2E_Test_Artifacts.zip`

---

## Viewing Reports
Double-click `app/appium-test/Test Results/HTML/execution-report.html` to view the interactive test suite dashboard.
