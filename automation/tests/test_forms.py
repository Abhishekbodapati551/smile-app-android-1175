import pytest
from automation.pages.start_page import StartPage
from automation.pages.login_page import LoginPage
from automation.pages.register_page import RegisterPage

class TestForms:
    MODULE = "Forms"

    @pytest.mark.parametrize("idx", range(1, 51))
    def test_form_cases(self, driver, idx):
        test_id = f"TC_FORM_{idx:03d}"
        start_page = StartPage(driver)
        login_page = LoginPage(driver)
        register_page = RegisterPage(driver)

        start_page.navigate_to_app()
        assert start_page.is_loaded() is True
        start_page.click_patient_login()
        login_page.click_signup("child")
        register_page.register(f"Test User {idx}", f"user{idx}@smile.com", "Secret123!")
        assert driver.current_url is not None
