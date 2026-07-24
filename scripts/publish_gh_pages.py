import os
import shutil
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_RESULTS_DIR = os.path.join(BASE_DIR, "app", "appium-test", "Test Results")
PAGES_DIR = os.path.join(BASE_DIR, "public_reports")

BUILD_NUMBER = os.getenv("GITHUB_RUN_NUMBER", "build-local")
if not BUILD_NUMBER.startswith("build-"):
    BUILD_NUMBER = f"build-{int(BUILD_NUMBER):03d}"

LATEST_DIR = os.path.join(PAGES_DIR, "reports", "latest")
HISTORY_BUILD_DIR = os.path.join(PAGES_DIR, "reports", "history", BUILD_NUMBER)

def publish_reports():
    print(f"Publishing reports to GitHub Pages structure for {BUILD_NUMBER}...")

    # Ensure target directories exist
    os.makedirs(LATEST_DIR, exist_ok=True)
    os.makedirs(HISTORY_BUILD_DIR, exist_ok=True)

    # 1. Copy HTML reports into latest/ and history/
    html_src = os.path.join(TEST_RESULTS_DIR, "HTML")
    if os.path.exists(html_src):
        for f in os.listdir(html_src):
            s_path = os.path.join(html_src, f)
            if os.path.isfile(s_path):
                shutil.copy2(s_path, os.path.join(LATEST_DIR, f))
                shutil.copy2(s_path, os.path.join(HISTORY_BUILD_DIR, f))

    # 2. Copy summary.md
    summary_src = os.path.join(TEST_RESULTS_DIR, "Summary", "summary.md")
    if os.path.exists(summary_src):
        shutil.copy2(summary_src, os.path.join(LATEST_DIR, "summary.md"))
        shutil.copy2(summary_src, os.path.join(HISTORY_BUILD_DIR, "summary.md"))

    # 3. Copy Excel reports
    excel_src = os.path.join(TEST_RESULTS_DIR, "Excel")
    if os.path.exists(excel_src):
        for f in os.listdir(excel_src):
            s_path = os.path.join(excel_src, f)
            if os.path.isfile(s_path):
                shutil.copy2(s_path, os.path.join(LATEST_DIR, f))
                shutil.copy2(s_path, os.path.join(HISTORY_BUILD_DIR, f))

    # 4. Copy ZIP artifact
    zip_src = os.path.join(TEST_RESULTS_DIR, "SmileApp_Android_Appium_E2E_Test_Artifacts.zip")
    if os.path.exists(zip_src):
        shutil.copy2(zip_src, os.path.join(LATEST_DIR, "SmileApp_Android_Appium_E2E_Test_Artifacts.zip"))
        shutil.copy2(zip_src, os.path.join(HISTORY_BUILD_DIR, "SmileApp_Android_Appium_E2E_Test_Artifacts.zip"))

    # 5. Copy screenshots and logs
    for sub in ["Screenshots", "Logs"]:
        sub_src = os.path.join(TEST_RESULTS_DIR, sub)
        if os.path.exists(sub_src):
            shutil.copytree(sub_src, os.path.join(LATEST_DIR, sub.lower()), dirs_exist_ok=True)
            shutil.copytree(sub_src, os.path.join(HISTORY_BUILD_DIR, sub.lower()), dirs_exist_ok=True)

    # 6. Create index.html at root of GitHub Pages site redirecting to latest execution report
    index_html_content = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=reports/latest/execution-report.html" />
    <title>SmileApp E2E Test Reports</title>
</head>
<body>
    <p>Redirecting to <a href="reports/latest/execution-report.html">SmileApp Latest Execution Report</a>...</p>
</body>
</html>
"""
    with open(os.path.join(PAGES_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html_content)

    print("GitHub Pages report structure generated successfully!")

if __name__ == "__main__":
    publish_reports()
