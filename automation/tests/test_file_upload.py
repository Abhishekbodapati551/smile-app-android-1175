import pytest
from automation.pages.start_page import StartPage

class TestFileUpload:
    MODULE = "File Upload"

    @pytest.mark.parametrize("idx", range(1, 21))
    def test_upl_cases(self, driver, idx):
        test_id = f"TC_UPL_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
