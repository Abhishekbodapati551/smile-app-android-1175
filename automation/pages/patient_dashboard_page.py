from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class PatientDashboardPage(BasePage):
    WELCOME_MSG = (By.ID, "child-welcome-msg")
    STREAK_TXT = (By.ID, "child-streak")
    START_MISSION_BTN = (By.ID, "btn-start-recording-main")
    SYNC_BTN = (By.XPATH, "//button[contains(text(), 'SYNC')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(text(), '⭐')]")
    POINTS_DISPLAY = (By.ID, "points-display")
    
    def is_dashboard_visible(self):
        return self.is_displayed(By.ID, "screen-dashboard-child")

    def get_welcome_text(self):
        return self.get_text(*self.WELCOME_MSG)

    def logout(self):
        self.click(*self.LOGOUT_BTN)
