from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class DoctorAppointmentsPage(BasePage):
    """Page Object for DoctorAppointmentManagerActivity."""

    BTN_ADD_APPOINTMENT = (AppiumBy.ID, "com.example.smileapp:id/btnAddAppointment")
    ET_PATIENT_EMAIL = (AppiumBy.ID, "com.example.smileapp:id/etApptPatientEmail")
    ET_APPT_DATE = (AppiumBy.ID, "com.example.smileapp:id/etApptDate")
    ET_APPT_TIME = (AppiumBy.ID, "com.example.smileapp:id/etApptTime")
    ET_APPT_NOTES = (AppiumBy.ID, "com.example.smileapp:id/etApptNotes")
    BTN_SUBMIT_APPOINTMENT = (AppiumBy.ID, "com.example.smileapp:id/btnSaveAppointment")
    RECYCLER_DOCTOR_APPTS = (AppiumBy.ID, "com.example.smileapp:id/rvDoctorAppointments")

    def click_add_appointment(self):
        self.click(*self.BTN_ADD_APPOINTMENT)

    def create_appointment(self, email, date, time, notes):
        self.send_keys(*self.ET_PATIENT_EMAIL, email)
        self.send_keys(*self.ET_APPT_DATE, date)
        self.send_keys(*self.ET_APPT_TIME, time)
        self.send_keys(*self.ET_APPT_NOTES, notes)
        self.click(*self.BTN_SUBMIT_APPOINTMENT)

    def get_appointments_count(self):
        return len(self.find_elements(*self.RECYCLER_DOCTOR_APPTS))
