import pytest
from automation.pages.start_page import StartPage

class TestNavigation:
    MODULE = "Navigation"

    @pytest.mark.parametrize("idx", range(1, 31))
    def test_nav_cases(self, driver, idx):
        test_id = f"TC_NAV_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert start_page.is_loaded() is True

        if idx % 2 == 1:
            start_page.click_patient_login()
        else:
            start_page.click_doctor_login()

        assert driver.current_url is not None
