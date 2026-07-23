from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class MainPage(BasePage):
    """Page Object for MainActivity (Role Selection & App Landing)."""

    # Locators
    BTN_CHILD_ROLE = (AppiumBy.ID, "com.example.smileapp:id/btnChildRole")
    BTN_DOCTOR_ROLE = (AppiumBy.ID, "com.example.smileapp:id/btnDoctorRole")
    TXT_TITLE = (AppiumBy.ID, "com.example.smileapp:id/tvAppTitle")
    TXT_SUBTITLE = (AppiumBy.ID, "com.example.smileapp:id/tvSubtitle")

    def click_child_role(self):
        """Navigate to Child Login screen."""
        self.click(*self.BTN_CHILD_ROLE)

    def click_doctor_role(self):
        """Navigate to Doctor Login screen."""
        self.click(*self.BTN_DOCTOR_ROLE)

    def is_main_screen_displayed(self):
        """Verify main role selection screen elements are visible."""
        return self.is_displayed(*self.BTN_CHILD_ROLE) and self.is_displayed(*self.BTN_DOCTOR_ROLE)
