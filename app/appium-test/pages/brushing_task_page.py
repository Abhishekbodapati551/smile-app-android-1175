from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class BrushingTaskPage(BasePage):
    """Page Object for BrushingTaskActivity (2-min Camera Brushing Timer)."""

    # Locators
    TV_TIMER_DISPLAY = (AppiumBy.ID, "com.example.smileapp:id/tvTimerDisplay")
    BTN_START_TIMER = (AppiumBy.ID, "com.example.smileapp:id/btnStartTimer")
    BTN_PAUSE_TIMER = (AppiumBy.ID, "com.example.smileapp:id/btnPauseTimer")
    BTN_FINISH_SESSION = (AppiumBy.ID, "com.example.smileapp:id/btnFinishBrushing")
    CAMERA_PREVIEW = (AppiumBy.ID, "com.example.smileapp:id/cameraPreview")
    TV_CAMERA_STATUS = (AppiumBy.ID, "com.example.smileapp:id/tvCameraStatus")

    def get_timer_value(self):
        return self.get_text(*self.TV_TIMER_DISPLAY)

    def start_timer(self):
        self.click(*self.BTN_START_TIMER)

    def pause_timer(self):
        self.click(*self.BTN_PAUSE_TIMER)

    def finish_session(self):
        self.click(*self.BTN_FINISH_SESSION)

    def is_camera_active(self):
        return self.is_displayed(*self.CAMERA_PREVIEW)
