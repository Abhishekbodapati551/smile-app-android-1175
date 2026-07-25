import pytest
import time
from automation.pages.start_page import StartPage

class TestPerformanceSmoke:
    MODULE = "Performance Smoke Tests"

    @pytest.mark.parametrize("idx", range(1, 21))
    def test_prf_cases(self, driver, idx):
        test_id = f"TC_PRF_{idx:03d}"
        t0 = time.time()
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        load_time = time.time() - t0
        assert load_time < 10.0
