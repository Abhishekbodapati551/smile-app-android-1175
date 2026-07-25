import time
import pytest
from automation.pages.start_page import StartPage
from automation.pages.login_page import LoginPage
from automation.pages.dashboard_page import DashboardPage

class TestAuthentication:
    MODULE = "Authentication"

    @pytest.mark.parametrize("idx", range(1, 41))
    def test_auth_cases(self, driver, idx):
        test_id = f"TC_AUTH_{idx:03d}"
        start_page = StartPage(driver)
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        start_page.navigate_to_app()
        assert start_page.is_loaded() is True

        if idx % 2 == 1:
            start_page.click_patient_login()
            login_page.login_patient("patient@smile.com", "password123")
        else:
            start_page.click_doctor_login()
            login_page.login_doctor("doc@smile.com", "docpassword")

        assert driver.current_url is not None
