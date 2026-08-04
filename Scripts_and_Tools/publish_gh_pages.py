import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_REPORTS_DIR = BASE_DIR / "public_reports"
PUBLIC_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Copy Appium Reports
appium_results = BASE_DIR / "Automation_Testing" / "Mobile_Appium_Tests" / "Test Results"
if appium_results.exists():
    shutil.copytree(appium_results, PUBLIC_REPORTS_DIR / "mobile_appium", dirs_exist_ok=True)
    print(f"Copied Appium test results to {PUBLIC_REPORTS_DIR / 'mobile_appium'}")

# 2. Copy Selenium Reports
selenium_results = BASE_DIR / "automation" / "reports"
if selenium_results.exists():
    shutil.copytree(selenium_results, PUBLIC_REPORTS_DIR / "web_selenium", dirs_exist_ok=True)
    print(f"Copied Selenium test results to {PUBLIC_REPORTS_DIR / 'web_selenium'}")

# 3. Create index landing for public_reports
index_file = PUBLIC_REPORTS_DIR / "index.html"
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Smile App Automation Test Reports</title>
    <style>
        body { font-family: sans-serif; padding: 40px; line-height: 1.6; background: #f8fafc; color: #1e293b; }
        .card { background: white; padding: 24px; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        h1 { color: #2563eb; }
        a { color: #2563eb; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>⭐ Smile App - E2E Automation Test Reports Dashboard</h1>
    <div class="card">
        <h2>📱 Mobile Appium E2E Reports (400+ TCs)</h2>
        <ul>
            <li><a href="mobile_appium/HTML/dashboard.html">HTML Executive Dashboard</a></li>
            <li><a href="mobile_appium/HTML/execution-report.html">Detailed Execution Report</a></li>
            <li><a href="mobile_appium/Excel/Automation_Test_Report.xlsx">Excel 6-Sheet Master Report</a></li>
        </ul>
    </div>
    <div class="card">
        <h2>🌐 Web Selenium E2E Reports (400+ TCs)</h2>
        <ul>
            <li><a href="web_selenium/HTML/dashboard.html">HTML Executive Dashboard</a></li>
            <li><a href="web_selenium/HTML/execution-report.html">Detailed Execution Report</a></li>
            <li><a href="web_selenium/Excel/Automation_Test_Report.xlsx">Excel 6-Sheet Master Report</a></li>
        </ul>
    </div>
</body>
</html>
"""
with open(index_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated index.html at {index_file}")
