from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class RegisterPage(BasePage):
    PATIENT_ROLE_BTN = (By.ID, "reg-role-child")
    DOCTOR_ROLE_BTN = (By.ID, "reg-role-doctor")
    NAME_INPUT = (By.ID, "reg-name")
    EMAIL_INPUT = (By.ID, "reg-email")
    PASSWORD_INPUT = (By.ID, "reg-password")
    DOCTOR_ID_INPUT = (By.ID, "reg-doctor-id")
    SIGNUP_BTN = (By.ID, "btn-signup")

    def register_patient(self, name, email, password):
        self.click(*self.PATIENT_ROLE_BTN)
        self.send_keys(*self.NAME_INPUT, name)
        self.send_keys(*self.EMAIL_INPUT, email)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.click(*self.SIGNUP_BTN)

    def register_doctor(self, name, email, password, doctor_id):
        self.click(*self.DOCTOR_ROLE_BTN)
        self.send_keys(*self.NAME_INPUT, name)
        self.send_keys(*self.EMAIL_INPUT, email)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.send_keys(*self.DOCTOR_ID_INPUT, doctor_id)
        self.click(*self.SIGNUP_BTN)
