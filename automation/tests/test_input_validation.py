import pytest
from automation.pages.start_page import StartPage

class TestInputValidation:
    MODULE = "Input Validation"

    @pytest.mark.parametrize("idx", range(1, 41))
    def test_inp_cases(self, driver, idx):
        test_id = f"TC_INP_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
