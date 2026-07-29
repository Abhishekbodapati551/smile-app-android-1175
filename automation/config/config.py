import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Base URL from Environment Variable - Default to Live GitHub Pages URL or local file fallback
DEFAULT_BASE_URL = "https://abhishekbodapati551.github.io/smile-app-android-1175/"
BASE_URL = os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip('/') + '/'

# Headless mode option
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Pass percentage threshold
PASS_THRESHOLD_PERCENT = float(os.getenv("PASS_THRESHOLD_PERCENT", "95.0"))

# Timeouts
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# Directories
REPORTS_DIR = BASE_DIR / "reports"
EXCEL_REPORTS_DIR = REPORTS_DIR / "Excel"
HTML_REPORTS_DIR = REPORTS_DIR / "HTML"
JSON_REPORTS_DIR = REPORTS_DIR / "JSON"
SUMMARY_REPORTS_DIR = REPORTS_DIR / "Summary"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"

# Ensure all directories exist
for folder in [REPORTS_DIR, EXCEL_REPORTS_DIR, HTML_REPORTS_DIR, JSON_REPORTS_DIR, SUMMARY_REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ZIP archive path
ZIP_PATH = BASE_DIR.parent / "smileapp-e2e-automation.zip"
