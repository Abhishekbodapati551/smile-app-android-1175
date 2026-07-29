from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class DoctorDashboardPage(BasePage):
    WELCOME_MSG = (By.ID, "doctor-welcome-msg")
    STAT_PATIENTS = (By.ID, "stat-patients")
    STAT_APPTS = (By.ID, "stat-appts")
    STAT_APPROVALS = (By.ID, "stat-approvals")
    STAT_REVIEWS = (By.ID, "stat-reviews")
    NEW_VISIT_BTN = (By.XPATH, "//button[contains(text(), '+ NEW VISIT')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(text(), '🚪')]")

    def is_dashboard_visible(self):
        return self.is_displayed(By.ID, "screen-dashboard-doctor")

    def get_welcome_text(self):
        return self.get_text(*self.WELCOME_MSG)

    def logout(self):
        self.click(*self.LOGOUT_BTN)
