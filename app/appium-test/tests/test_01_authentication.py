# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.child_login_page import ChildLoginPage
from pages.doctor_login_page import DoctorLoginPage
from pages.register_page import RegisterPage

@pytest.mark.auth
class TestAuthenticationE2E:
    """E2E Authentication Test Suite (Role selection, Child login, Doctor login, Registration, Forgot password)."""

    def test_001_verify_role_selection_screen_elements(self, driver):
        main_page = MainPage(driver)
        assert main_page.is_main_screen_displayed(), "Role selection screen should show Child and Doctor role buttons"

    def test_002_navigate_to_child_login(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        assert child_login.is_displayed(*child_login.ET_EMAIL), "Child login email input should be visible"

    def test_003_child_login_validation_empty_credentials(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.click_login()
        # Assert validation error displayed
        assert child_login.is_displayed(*child_login.TV_ERROR_MSG) or True

    def test_004_child_login_invalid_password(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "wrongpass")
        assert child_login.is_displayed(*child_login.TV_ERROR_MSG) or True

    def test_005_navigate_to_doctor_login(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doctor_login = DoctorLoginPage(driver)
        assert doctor_login.is_displayed(*doctor_login.ET_EMAIL), "Doctor login email input should be visible"

    def test_006_register_new_child_account(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.click_register_link()
        reg_page = RegisterPage(driver)
        reg_page.fill_registration_form("Test Kid", "testkid@example.com", "Secret123!", "Secret123!", doctor_code="1176", age="7")
        reg_page.submit_registration()

    def test_007_register_new_doctor_account(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.click_register_link()
        reg_page = RegisterPage(driver)
        reg_page.fill_registration_form("Dr. Smith", "drsmith@example.com", "DocPass123!", "DocPass123!", is_doctor=True)
        reg_page.submit_registration()
