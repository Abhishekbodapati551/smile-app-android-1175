from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class ChildLoginPage(BasePage):
    """Page Object for ChildLoginActivity."""

    # Locators
    ET_EMAIL = (AppiumBy.ID, "com.example.smileapp:id/etChildEmail")
    ET_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/etChildPassword")
    BTN_LOGIN = (AppiumBy.ID, "com.example.smileapp:id/btnChildLogin")
    TV_REGISTER = (AppiumBy.ID, "com.example.smileapp:id/tvGoToRegister")
    TV_FORGOT_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/tvForgotPassword")
    TV_ERROR_MSG = (AppiumBy.ID, "com.example.smileapp:id/tvErrorMessage")

    def enter_email(self, email):
        self.send_keys(*self.ET_EMAIL, email)

    def enter_password(self, password):
        self.send_keys(*self.ET_PASSWORD, password)

    def click_login(self):
        self.click(*self.BTN_LOGIN)

    def click_register_link(self):
        self.click(*self.TV_REGISTER)

    def click_forgot_password_link(self):
        self.click(*self.TV_FORGOT_PASSWORD)

    def login_as_child(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        return self.get_text(*self.TV_ERROR_MSG) if self.is_displayed(*self.TV_ERROR_MSG) else ""
