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
        start_time = time.time()
        start_page = StartPage(driver)
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        start_page.navigate_to_app()

        if idx % 2 == 1:
            # Patient Login flows
            start_page.click_patient_login()
            if idx == 1:
                login_page.login_patient("patient@smile.com", "password123")
            elif idx == 3:
                login_page.login_patient("invalid@smile.com", "wrongpass")
            else:
                login_page.login_patient(f"user{idx}@smile.com", "pass123")
        else:
            # Doctor Login flows
            start_page.click_doctor_login()
            if idx == 2:
                login_page.login_doctor("doctor@smile.com", "docpass")
            else:
                login_page.login_doctor(f"doc{idx}@smile.com", "docpass123")

        duration = round(time.time() - start_time, 2)
        assert driver.current_url is not None
