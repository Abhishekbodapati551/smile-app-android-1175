from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators based on index.html
    START_PATIENT_BTN = (By.XPATH, "//button[contains(text(), \"I'M A PATIENT\")]")
    START_DOCTOR_BTN = (By.XPATH, "//button[contains(text(), \"I'M A DOCTOR\")]")
    
    CHILD_EMAIL_INPUT = (By.ID, "child-email")
    CHILD_PASS_INPUT = (By.ID, "child-password")
    CHILD_LOGIN_BTN = (By.ID, "btn-login-child")
    
    DOCTOR_EMAIL_INPUT = (By.ID, "doctor-email")
    DOCTOR_PASS_INPUT = (By.ID, "doctor-password")
    DOCTOR_LOGIN_BTN = (By.ID, "btn-login-doctor")
    
    REGISTER_LINK = (By.XPATH, "//span[contains(text(), 'Sign Up') or contains(text(), 'Register')]")
    
    def open_start(self, url):
        self.navigate_to(url)

    def select_patient_portal(self):
        self.click(*self.START_PATIENT_BTN)

    def select_doctor_portal(self):
        self.click(*self.START_DOCTOR_BTN)

    def login_patient(self, email, password):
        self.select_patient_portal()
        self.send_keys(*self.CHILD_EMAIL_INPUT, email)
        self.send_keys(*self.CHILD_PASS_INPUT, password)
        self.click(*self.CHILD_LOGIN_BTN)

    def login_doctor(self, email, password):
        self.select_doctor_portal()
        self.send_keys(*self.DOCTOR_EMAIL_INPUT, email)
        self.send_keys(*self.DOCTOR_PASS_INPUT, password)
        self.click(*self.DOCTOR_LOGIN_BTN)
