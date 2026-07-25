from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class RegisterPage(BasePage):
    REGISTER_SCREEN = (By.ID, "screen-register")
    ROLE_CHILD_BTN = (By.ID, "reg-role-child")
    ROLE_DOCTOR_BTN = (By.ID, "reg-role-doctor")
    NAME_INPUT = (By.ID, "reg-name")
    EMAIL_INPUT = (By.ID, "reg-email")
    PASSWORD_INPUT = (By.ID, "reg-password")
    DOCTOR_ID_INPUT = (By.ID, "reg-doctor-id")
    SIGNUP_BTN = (By.ID, "btn-signup")
    LOGIN_LINK = (By.XPATH, "//div[@id='screen-register']//span[contains(text(), 'Login')]")

    def select_role(self, role: str):
        if role.lower() == "doctor":
            self.js_click(*self.ROLE_DOCTOR_BTN)
        else:
            self.js_click(*self.ROLE_CHILD_BTN)

    def register(self, name: str, email: str, password: str, doctor_id: str = ""):
        self.type_text(*self.NAME_INPUT, name)
        self.type_text(*self.EMAIL_INPUT, email)
        self.type_text(*self.PASSWORD_INPUT, password)
        if doctor_id:
            self.type_text(*self.DOCTOR_ID_INPUT, doctor_id)
        self.js_click(*self.SIGNUP_BTN)
