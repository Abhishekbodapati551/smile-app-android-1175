from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class RegisterPage(BasePage):
    """Page Object for RegisterActivity."""

    # Locators
    ET_FULL_NAME = (AppiumBy.ID, "com.example.smileapp:id/etFullName")
    ET_EMAIL = (AppiumBy.ID, "com.example.smileapp:id/etRegisterEmail")
    ET_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/etRegisterPassword")
    ET_CONFIRM_PASSWORD = (AppiumBy.ID, "com.example.smileapp:id/etConfirmPassword")
    ET_DOCTOR_ID = (AppiumBy.ID, "com.example.smileapp:id/etDoctorCode")
    ET_AGE = (AppiumBy.ID, "com.example.smileapp:id/etChildAge")
    RADIO_CHILD = (AppiumBy.ID, "com.example.smileapp:id/rbChildRole")
    RADIO_DOCTOR = (AppiumBy.ID, "com.example.smileapp:id/rbDoctorRole")
    BTN_REGISTER = (AppiumBy.ID, "com.example.smileapp:id/btnRegisterSubmit")
    TV_LOGIN_LINK = (AppiumBy.ID, "com.example.smileapp:id/tvBackToLogin")

    def fill_registration_form(self, name, email, password, confirm_pwd, doctor_code="1176", age="8", is_doctor=False):
        self.send_keys(*self.ET_FULL_NAME, name)
        self.send_keys(*self.ET_EMAIL, email)
        self.send_keys(*self.ET_PASSWORD, password)
        self.send_keys(*self.ET_CONFIRM_PASSWORD, confirm_pwd)
        
        if is_doctor:
            self.click(*self.RADIO_DOCTOR)
        else:
            self.click(*self.RADIO_CHILD)
            if self.is_displayed(*self.ET_DOCTOR_ID):
                self.send_keys(*self.ET_DOCTOR_ID, doctor_code)
            if self.is_displayed(*self.ET_AGE):
                self.send_keys(*self.ET_AGE, age)

    def submit_registration(self):
        self.click(*self.BTN_REGISTER)

    def back_to_login(self):
        self.click(*self.TV_LOGIN_LINK)
