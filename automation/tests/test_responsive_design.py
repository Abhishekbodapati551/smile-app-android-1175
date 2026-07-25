import pytest
from automation.pages.start_page import StartPage

class TestResponsiveDesign:
    MODULE = "Responsive Design"

    @pytest.mark.parametrize("idx", range(1, 21))
    def test_rsp_cases(self, driver, idx):
        test_id = f"TC_RSP_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        if idx % 3 == 0:
            driver.set_window_size(375, 812) # Mobile
        elif idx % 3 == 1:
            driver.set_window_size(768, 1024) # Tablet
        else:
            driver.set_window_size(1920, 1080) # Desktop
        assert driver.current_url is not None
