from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from automation.config.config import HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

def create_driver(headless=HEADLESS):
    """
    Factory method to create a Selenium Chrome WebDriver instance.
    Configured for GitHub Actions headless environment and local execution.
    """
    options = Options()
    
    if headless:
        options.add_argument("--headless=new")
    
    # Chrome flags essential for CI runner environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        # Fallback without explicit driver manager if Chrome is in PATH
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver
