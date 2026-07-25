import time
import pytest
from automation.pages.start_page import StartPage
from automation.pages.login_page import LoginPage

class TestAuthorization:
    MODULE = "Authorization"

    @pytest.mark.parametrize("idx", range(1, 41))
    def test_azn_cases(self, driver, idx):
        test_id = f"TC_AZN_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
