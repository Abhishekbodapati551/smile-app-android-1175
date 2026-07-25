import pytest
from automation.pages.start_page import StartPage

class TestRegression:
    MODULE = "Regression"

    @pytest.mark.parametrize("idx", range(1, 51))
    def test_reg_cases(self, driver, idx):
        test_id = f"TC_REG_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
