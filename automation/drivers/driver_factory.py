import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from automation.config.config import HEADLESS, PAGE_LOAD_TIMEOUT

logger = logging.getLogger("DriverFactory")

class DriverFactory:
    @staticmethod
    def create_driver(headless: bool = HEADLESS):
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(2)
        logger.info(f"Initialized Chrome Driver (Headless: {headless})")
        return driver
