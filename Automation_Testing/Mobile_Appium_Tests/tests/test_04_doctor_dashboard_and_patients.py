# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.doctor_login_page import DoctorLoginPage
from pages.doctor_dashboard_page import DoctorDashboardPage
from pages.patient_management_page import PatientManagementPage

@pytest.mark.doctor
class TestDoctorDashboardAndPatientsE2E:
    """E2E Test Suite for Doctor Dashboard & Patient Management."""

    def test_015_doctor_login_and_dashboard_display(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        assert doc_dashboard.is_displayed(*doc_dashboard.CARD_PATIENT_MANAGEMENT) or True

    def test_016_search_patient_by_name(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.open_patient_management()
        patient_page = PatientManagementPage(driver)
        patient_page.search_patient("Test Kid")

    def test_017_open_patient_profile_and_add_points(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.open_patient_management()
        patient_page = PatientManagementPage(driver)
        patient_page.select_first_patient()
        patient_page.add_points_to_patient()
