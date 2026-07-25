import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from automation.config.config import BASE_URL, EXPLICIT_WAIT_TIMEOUT
from automation.utils.logger import logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_TIMEOUT)

    def navigate_to_app(self, relative_path: str = ""):
        target_url = BASE_URL + relative_path.lstrip("/")
        logger.info(f"Navigating to {target_url}")
        self.driver.get(target_url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def find_element(self, by: By, value: str):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by: By, value: str):
        return self.driver.find_elements(by, value)

    def click(self, by: By, value: str):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def js_click(self, by: By, value: str):
        element = self.find_element(by, value)
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, by: By, value: str, text: str):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by: By, value: str) -> str:
        element = self.find_element(by, value)
        return element.text

    def is_displayed(self, by: By, value: str) -> bool:
        try:
            elem = self.driver.find_element(by, value)
            return elem.is_displayed()
        except Exception:
            return False

    def is_visible(self, by: By, value: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
            return True
        except Exception:
            return False

    def get_browser_logs(self):
        try:
            return self.driver.get_log("browser")
        except Exception:
            return []
