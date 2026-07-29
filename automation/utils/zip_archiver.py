import os
import zipfile
from pathlib import Path
from automation.config.config import REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR, ZIP_PATH
from automation.utils.logger import get_logger

logger = get_logger("ZipArchiver")

def archive_results():
    """
    Bundles all reports, screenshots, logs into smileapp-e2e-automation.zip
    """
    logger.info(f"Creating ZIP archive at {ZIP_PATH}...")

    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add reports
        for root, _, files in os.walk(REPORTS_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = Path("reports") / file_path.relative_to(REPORTS_DIR)
                zipf.write(file_path, arcname)

        # Add screenshots
        for root, _, files in os.walk(SCREENSHOTS_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = Path("screenshots") / file_path.relative_to(SCREENSHOTS_DIR)
                zipf.write(file_path, arcname)

        # Add logs
        for root, _, files in os.walk(LOGS_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = Path("logs") / file_path.relative_to(LOGS_DIR)
                zipf.write(file_path, arcname)

    logger.info(f"Successfully archived test execution assets to {ZIP_PATH} (Size: {ZIP_PATH.stat().st_size} bytes)")
    return str(ZIP_PATH)
