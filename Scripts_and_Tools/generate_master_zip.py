import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MASTER_ZIP_PATH = BASE_DIR / "SmileApp_Master_E2E_Test_Reports.zip"

print(f"Creating Master E2E ZIP Archive at {MASTER_ZIP_PATH}...")

added_files = set()

with zipfile.ZipFile(MASTER_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Add Web Selenium Reports
    selenium_dir = BASE_DIR / "automation" / "reports"
    if selenium_dir.exists():
        for root, _, files in os.walk(selenium_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = str(Path("Web_Selenium_Reports") / file_path.relative_to(selenium_dir))
                if arcname not in added_files:
                    zipf.write(file_path, arcname)
                    added_files.add(arcname)

    selenium_zip = BASE_DIR / "smileapp-e2e-automation.zip"
    if selenium_zip.exists() and "Web_Selenium_Reports/smileapp-e2e-automation.zip" not in added_files:
        zipf.write(selenium_zip, "Web_Selenium_Reports/smileapp-e2e-automation.zip")
        added_files.add("Web_Selenium_Reports/smileapp-e2e-automation.zip")

    # 2. Add Mobile Appium Reports
    appium_dir = BASE_DIR / "Automation_Testing" / "Mobile_Appium_Tests" / "Test Results"
    if appium_dir.exists():
        for root, _, files in os.walk(appium_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = str(Path("Mobile_Appium_Reports") / file_path.relative_to(appium_dir))
                if arcname not in added_files:
                    zipf.write(file_path, arcname)
                    added_files.add(arcname)

    appium_zip = BASE_DIR / "Automation_Testing" / "Mobile_Appium_Tests" / "SmileApp_Android_Appium_E2E_Test_Artifacts.zip"
    if appium_zip.exists() and "Mobile_Appium_Reports/SmileApp_Android_Appium_E2E_Test_Artifacts.zip" not in added_files:
        zipf.write(appium_zip, "Mobile_Appium_Reports/SmileApp_Android_Appium_E2E_Test_Artifacts.zip")
        added_files.add("Mobile_Appium_Reports/SmileApp_Android_Appium_E2E_Test_Artifacts.zip")

print(f"Successfully generated Master ZIP: {MASTER_ZIP_PATH} (Size: {MASTER_ZIP_PATH.stat().st_size if MASTER_ZIP_PATH.exists() else 0} bytes)")
