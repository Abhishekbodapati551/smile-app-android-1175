import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from config import EXPLICIT_WAIT_TIMEOUT

class BasePage:
    """Base Page Object class encapsulating common driver actions and explicit wait wrappers."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT_TIMEOUT)

    def find_element(self, by, locator, timeout=EXPLICIT_WAIT_TIMEOUT):
        """Wait for and find a single UI element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def find_elements(self, by, locator, timeout=EXPLICIT_WAIT_TIMEOUT):
        """Wait for and find multiple UI elements."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, locator))
            )
        except Exception:
            return []

    def click(self, by, locator):
        """Wait for element to be clickable and click it."""
        element = WebDriverWait(self.driver, EXPLICIT_WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def send_keys(self, by, locator, text):
        """Clear existing text and type new text into input field."""
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, locator):
        """Get visible text from UI element."""
        element = self.find_element(by, locator)
        return element.text

    def is_displayed(self, by, locator, timeout=5):
        """Check if an element is currently displayed on screen."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            ).is_displayed()
        except Exception:
            return False

    def click_by_id(self, resource_id):
        """Click element by Android resource ID."""
        self.click(AppiumBy.ID, f"com.example.smileapp:id/{resource_id}")

    def send_keys_by_id(self, resource_id, text):
        """Type text into element specified by Android resource ID."""
        self.send_keys(AppiumBy.ID, f"com.example.smileapp:id/{resource_id}", text)

    def get_text_by_id(self, resource_id):
        """Get text from element specified by Android resource ID."""
        return self.get_text(AppiumBy.ID, f"com.example.smileapp:id/{resource_id}")

    def swipe_down(self):
        """Perform a standard swipe down gesture."""
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        start_x = int(size['width'] * 0.5)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def take_screenshot(self, filename):
        """Save a screenshot of current device screen."""
        self.driver.save_screenshot(filename)
