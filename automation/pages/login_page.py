from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class LoginPage(BasePage):
    CHILD_LOGIN_SCREEN = (By.ID, "screen-login-child")
    CHILD_EMAIL_INPUT = (By.ID, "child-email")
    CHILD_PASS_INPUT = (By.ID, "child-password")
    CHILD_SUBMIT_BTN = (By.ID, "btn-login-child")

    DOCTOR_LOGIN_SCREEN = (By.ID, "screen-login-doctor")
    DOCTOR_EMAIL_INPUT = (By.ID, "doctor-email")
    DOCTOR_PASS_INPUT = (By.ID, "doctor-password")
    DOCTOR_SUBMIT_BTN = (By.ID, "btn-login-doctor")

    SIGNUP_LINK_CHILD = (By.XPATH, "//div[@id='screen-login-child']//span[contains(text(), 'Sign Up')]")
    SIGNUP_LINK_DOCTOR = (By.XPATH, "//div[@id='screen-login-doctor']//span[contains(text(), 'Register')]")
    BACK_BTN_CHILD = (By.XPATH, "//div[@id='screen-login-child']//button[contains(text(), 'Back')]")

    def login_patient(self, email: str, password: str):
        self.type_text(*self.CHILD_EMAIL_INPUT, email)
        self.type_text(*self.CHILD_PASS_INPUT, password)
        self.js_click(*self.CHILD_SUBMIT_BTN)

    def login_doctor(self, email: str, password: str):
        self.type_text(*self.DOCTOR_EMAIL_INPUT, email)
        self.type_text(*self.DOCTOR_PASS_INPUT, password)
        self.js_click(*self.DOCTOR_SUBMIT_BTN)

    def click_signup(self, role: str = "child"):
        if role == "doctor":
            self.js_click(*self.SIGNUP_LINK_DOCTOR)
        else:
            self.js_click(*self.SIGNUP_LINK_CHILD)
