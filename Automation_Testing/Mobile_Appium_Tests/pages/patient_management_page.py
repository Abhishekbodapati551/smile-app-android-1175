from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class PatientManagementPage(BasePage):
    """Page Object for PatientManagementActivity & PatientProfileActivity."""

    ET_SEARCH_PATIENT = (AppiumBy.ID, "com.example.smileapp:id/etSearchPatient")
    RECYCLER_PATIENTS = (AppiumBy.ID, "com.example.smileapp:id/rvPatientList")
    TV_PATIENT_NAME = (AppiumBy.ID, "com.example.smileapp:id/tvPatientName")
    TV_PATIENT_STREAK = (AppiumBy.ID, "com.example.smileapp:id/tvPatientStreak")
    BTN_ADD_POINTS = (AppiumBy.ID, "com.example.smileapp:id/btnAddPoints")
    BTN_SCHEDULE_VISIT = (AppiumBy.ID, "com.example.smileapp:id/btnScheduleVisit")

    def search_patient(self, query):
        self.send_keys(*self.ET_SEARCH_PATIENT, query)

    def get_patient_list(self):
        return self.find_elements(*self.RECYCLER_PATIENTS)

    def select_first_patient(self):
        patients = self.get_patient_list()
        if patients:
            patients[0].click()

    def add_points_to_patient(self):
        self.click(*self.BTN_ADD_POINTS)

    def schedule_visit_for_patient(self):
        self.click(*self.BTN_SCHEDULE_VISIT)
