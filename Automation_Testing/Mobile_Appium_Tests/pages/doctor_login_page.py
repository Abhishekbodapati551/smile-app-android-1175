from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class DoctorLoginPage(BasePage):
    """Page Object for DoctorLoginActivity."""

    # Locators
    ET_EMAIL = (AppiumBy.ID, "com.example.smileapp:id/etDoctorEmail")
    ET_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/etDoctorPassword")
    BTN_LOGIN = (AppiumBy.ID, "com.example.smileapp:id/btnDoctorLogin")
    TV_REGISTER = (AppiumBy.ID, "com.example.smileapp:id/tvGoToDoctorRegister")
    TV_FORGOT_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/tvDoctorForgotPassword")
    TV_ERROR_MSG = (AppiumBy.ID, "com.example.smileapp:id/tvDoctorError")

    def enter_email(self, email):
        self.send_keys(*self.ET_EMAIL, email)

    def enter_password(self, password):
        self.send_keys(*self.ET_PASSWORD, password)

    def click_login(self):
        self.click(*self.BTN_LOGIN)

    def click_register_link(self):
        self.click(*self.TV_REGISTER)

    def login_as_doctor(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.get_text(*self.TV_ERROR_MSG) if self.is_displayed(*self.TV_ERROR_MSG) else ""
