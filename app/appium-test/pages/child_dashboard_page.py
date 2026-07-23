from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class ChildDashboardPage(BasePage):
    """Page Object for ChildDashboardActivity."""

    # Locators
    TV_WELCOME_NAME = (AppiumBy.ID, "com.example.smileapp:id/tvWelcomeChild")
    TV_STREAK_COUNT = (AppiumBy.ID, "com.example.smileapp:id/tvStreakCount")
    TV_POINTS_COUNT = (AppiumBy.ID, "com.example.smileapp:id/tvPointsCount")
    BTN_START_BRUSHING = (AppiumBy.ID, "com.example.smileapp:id/btnStartBrushing")
    BTN_REWARDS = (AppiumBy.ID, "com.example.smileapp:id/btnGoToRewards")
    BTN_APPOINTMENTS = (AppiumBy.ID, "com.example.smileapp:id/btnChildAppointments")
    BTN_BRUSHING_TIPS = (AppiumBy.ID, "com.example.smileapp:id/btnBrushingTips")
    BTN_LOGOUT = (AppiumBy.ID, "com.example.smileapp:id/btnChildLogout")

    def get_welcome_text(self):
        return self.get_text(*self.TV_WELCOME_NAME)

    def get_streak_count(self):
        return self.get_text(*self.TV_STREAK_COUNT)

    def get_points_count(self):
        return self.get_text(*self.TV_POINTS_COUNT)

    def open_brushing_task(self):
        self.click(*self.BTN_START_BRUSHING)

    def open_rewards(self):
        self.click(*self.BTN_REWARDS)

    def open_appointments(self):
        self.click(*self.BTN_APPOINTMENTS)

    def open_tips(self):
        self.click(*self.BTN_BRUSHING_TIPS)

    def logout(self):
        self.click(*self.BTN_LOGOUT)
