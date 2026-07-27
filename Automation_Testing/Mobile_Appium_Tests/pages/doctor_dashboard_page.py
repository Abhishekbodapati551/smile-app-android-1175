from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class DoctorDashboardPage(BasePage):
    """Page Object for DoctorDashboardActivity."""

    TV_WELCOME_DOCTOR = (AppiumBy.ID, "com.example.smileapp:id/tvWelcomeDoctor")
    TV_DOCTOR_CODE = (AppiumBy.ID, "com.example.smileapp:id/tvDoctorCodeDisplay")
    CARD_PATIENT_MANAGEMENT = (AppiumBy.ID, "com.example.smileapp:id/cardPatientManagement")
    CARD_PENDING_APPROVALS = (AppiumBy.ID, "com.example.smileapp:id/cardPendingApprovals")
    CARD_VIDEO_REVIEWS = (AppiumBy.ID, "com.example.smileapp:id/cardVideoReviews")
    CARD_APPOINTMENTS = (AppiumBy.ID, "com.example.smileapp:id/cardAppointments")
    BTN_PROFILE = (AppiumBy.ID, "com.example.smileapp:id/btnDoctorProfile")
    BTN_LOGOUT = (AppiumBy.ID, "com.example.smileapp:id/btnDoctorLogout")

    def get_welcome_text(self):
        return self.get_text(*self.TV_WELCOME_DOCTOR)

    def get_doctor_code(self):
        return self.get_text(*self.TV_DOCTOR_CODE)

    def open_patient_management(self):
        self.click(*self.CARD_PATIENT_MANAGEMENT)

    def open_pending_approvals(self):
        self.click(*self.CARD_PENDING_APPROVALS)

    def open_video_reviews(self):
        self.click(*self.CARD_VIDEO_REVIEWS)

    def open_appointments(self):
        self.click(*self.CARD_APPOINTMENTS)

    def open_profile(self):
        self.click(*self.BTN_PROFILE)

    def logout(self):
        self.click(*self.BTN_LOGOUT)
