from selenium.webdriver.common.by import By
from automation.pages.base_page import BasePage

class StartPage(BasePage):
    START_SCREEN = (By.ID, "screen-start")
    PATIENT_BTN = (By.XPATH, "//button[contains(text(), \"I'M A PATIENT\")]")
    DOCTOR_BTN = (By.XPATH, "//button[contains(text(), \"I'M A DOCTOR\")]")
    APP_HEADER = (By.XPATH, "//h1[contains(text(), 'Smile App')]")

    def is_loaded(self) -> bool:
        return self.is_visible(*self.START_SCREEN, timeout=10)

    def click_patient_login(self):
        self.js_click(*self.PATIENT_BTN)

    def click_doctor_login(self):
        self.js_click(*self.DOCTOR_BTN)
