import os
import sys
from pathlib import Path

# Base Paths
AUTOMATION_ROOT = Path(__file__).parent.parent.resolve()
PROJECT_ROOT = AUTOMATION_ROOT.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Reports & Artifact Paths
REPORTS_DIR = AUTOMATION_ROOT / "reports"
EXCEL_REPORTS_DIR = REPORTS_DIR / "Excel"
HTML_REPORTS_DIR = REPORTS_DIR / "HTML"
JSON_REPORTS_DIR = REPORTS_DIR / "JSON"
SUMMARY_REPORTS_DIR = REPORTS_DIR / "Summary"
SCREENSHOTS_DIR = AUTOMATION_ROOT / "screenshots"
LOGS_DIR = AUTOMATION_ROOT / "logs"

# Base URL Configuration (Configurable via BASE_URL environment variable)
# Default fallback to GitHub Pages deployment pattern
DEFAULT_BASE_URL = os.environ.get("BASE_URL", "https://abhishekbodapati551.github.io/smile-app-android-1175/")
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"

# Driver & Execution Settings
HEADLESS = os.environ.get("HEADLESS", "true").lower() in ("true", "1", "yes")
EXPLICIT_WAIT_TIMEOUT = int(os.environ.get("EXPLICIT_WAIT_TIMEOUT", "10"))
PAGE_LOAD_TIMEOUT = int(os.environ.get("PAGE_LOAD_TIMEOUT", "20"))
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", "2"))
PASS_THRESHOLD_PERCENT = float(os.environ.get("PASS_THRESHOLD_PERCENT", "95.0"))

# Ensure directories exist
for folder in [REPORTS_DIR, EXCEL_REPORTS_DIR, HTML_REPORTS_DIR, JSON_REPORTS_DIR, SUMMARY_REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
