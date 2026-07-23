from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class ChildAppointmentsPage(BasePage):
    """Page Object for ChildAppointmentsActivity."""

    RECYCLER_APPOINTMENTS = (AppiumBy.ID, "com.example.smileapp:id/rvAppointments")
    TV_NO_APPOINTMENTS = (AppiumBy.ID, "com.example.smileapp:id/tvNoAppointments")

    def get_appointments_list(self):
        return self.find_elements(*self.RECYCLER_APPOINTMENTS)

    def has_no_appointments_message(self):
        return self.is_displayed(*self.TV_NO_APPOINTMENTS)
