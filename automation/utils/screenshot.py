import os
import time
from pathlib import Path
from automation.config.config import SCREENSHOTS_DIR
from automation.utils.logger import get_logger

logger = get_logger("ScreenshotUtility")

def capture_screenshot(driver, test_id, name="screenshot"):
    """
    Captures a screenshot of the browser window and saves it to screenshots directory.
    Returns relative path to screenshot.
    """
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in name if c.isalnum() or c in ('_', '-'))
        filename = f"{test_id}_{safe_name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        driver.save_screenshot(str(filepath))
        logger.info(f"Captured screenshot for {test_id}: {filepath}")
        return str(filepath.relative_to(SCREENSHOTS_DIR.parent))
    except Exception as e:
        logger.error(f"Failed to capture screenshot for {test_id}: {e}")
        return ""
