import pytest
from automation.pages.start_page import StartPage

class TestUIValidation:
    MODULE = "UI Validation"

    @pytest.mark.parametrize("idx", range(1, 51))
    def test_ui_cases(self, driver, idx):
        test_id = f"TC_UI_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert start_page.is_loaded() is True
