import sys
import os
import requests
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from automation.config.config import BASE_URL
from automation.utils.logger import get_logger

logger = get_logger("DeploymentVerifier")

def verify_deployment(url=BASE_URL):
    logger.info(f"Starting Deployment Verification for URL: {url}")
    
    if url.startswith("file://") or "localhost" in url:
        logger.info(f"Local file/url detected ({url}), bypassing HTTP GET request check.")
        return True

    try:
        response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        logger.info(f"Deployment HTTP Status Code: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Deployment Verification Failed! HTTP Status: {response.status_code}")
            return False
            
        content = response.text
        if "Smile App" not in content and "<html" not in content.lower():
            logger.error("Deployment Verification Failed! Expected application HTML markup not found.")
            return False
            
        logger.info("✓ Deployment Verification PASSED: Application is live and serving HTTP 200.")
        return True

    except Exception as e:
        logger.error(f"Deployment Verification Exception: {e}")
        return False

if __name__ == "__main__":
    target_url = os.getenv("BASE_URL", BASE_URL)
    success = verify_deployment(target_url)
    if not success:
        sys.exit(1)
    sys.exit(0)
