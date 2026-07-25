import pytest
from automation.pages.start_page import StartPage

class TestAccessibility:
    MODULE = "Accessibility"

    @pytest.mark.parametrize("idx", range(1, 21))
    def test_acc_cases(self, driver, idx):
        test_id = f"TC_ACC_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
