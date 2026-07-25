import sys
import logging
import requests
from automation.config.config import BASE_URL
from automation.utils.logger import logger

class DeploymentVerifier:
    @staticmethod
    def verify_deployment(url: str = BASE_URL) -> bool:
        logger.info(f"--- Stage 7: Verifying Live Deployment Availability at {url} ---")
        try:
            if url.startswith("file://"):
                file_path = url.replace("file:///", "").replace("file://", "").rstrip("/")
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                status_code = 200
            else:
                response = requests.get(url, timeout=15)
                status_code = response.status_code
                html_content = response.text

            logger.info(f"Deployment Check {url} -> Status Code: {status_code}")
            
            if status_code != 200:
                logger.error(f"Deployment verification failed: Expected status 200, got {status_code}")
                return False

            if not html_content or "<html" not in html_content.lower():
                logger.error("Deployment verification failed: HTML content is empty or invalid.")
                return False

            if "Smile App" not in html_content and "screen-start" not in html_content:
                logger.error("Deployment verification failed: Main page elements missing in HTML.")
                return False

            logger.info("✓ Live Deployment verification PASSED successfully!")
            return True

        except Exception as e:
            logger.error(f"Deployment verification encountered an exception: {e}")
            return False

if __name__ == "__main__":
    success = DeploymentVerifier.verify_deployment()
    if not success:
        sys.exit(1)
    sys.exit(0)
