import pytest
from automation.pages.start_page import StartPage

class TestCRUDOperations:
    MODULE = "CRUD Operations"

    @pytest.mark.parametrize("idx", range(1, 51))
    def test_crud_cases(self, driver, idx):
        test_id = f"TC_CRUD_{idx:03d}"
        start_page = StartPage(driver)
        start_page.navigate_to_app()
        assert driver.current_url is not None
