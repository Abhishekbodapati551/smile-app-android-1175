import time
from pathlib import Path
from automation.config.config import SCREENSHOTS_DIR
from automation.utils.logger import logger

class ScreenshotUtil:
    @staticmethod
    def capture_screenshot(driver, test_id: str, suffix: str = "failure") -> str:
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{test_id}_{suffix}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename
            driver.save_screenshot(str(filepath))
            logger.info(f"Saved screenshot: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to capture screenshot for test {test_id}: {e}")
            return ""
