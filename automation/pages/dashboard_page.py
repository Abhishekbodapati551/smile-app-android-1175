from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class DashboardPage(BasePage):
    CHILD_DASHBOARD = (By.ID, "screen-dashboard-child")
    DOCTOR_DASHBOARD = (By.ID, "screen-dashboard-doctor")
    CHILD_WELCOME_MSG = (By.ID, "child-welcome-msg")
    LOGOUT_BTN = (By.XPATH, "//button[contains(text(), '⭐') or contains(text(), 'Logout')]")

    def is_child_dashboard_displayed(self) -> bool:
        return self.is_visible(*self.CHILD_DASHBOARD)

    def is_doctor_dashboard_displayed(self) -> bool:
        return self.is_visible(*self.DOCTOR_DASHBOARD)
