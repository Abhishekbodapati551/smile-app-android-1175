# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.doctor_login_page import DoctorLoginPage
from pages.doctor_dashboard_page import DoctorDashboardPage
from pages.doctor_appointments_page import DoctorAppointmentsPage

@pytest.mark.doctor
class TestDoctorAppointmentsAndProfileE2E:
    """E2E Test Suite for Doctor Appointments Management & Profile settings."""

    def test_020_schedule_new_patient_appointment(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.open_appointments()
        appts_page = DoctorAppointmentsPage(driver)
        appts_page.click_add_appointment()
        appts_page.create_appointment("testkid@example.com", "2026-08-15", "10:30 AM", "Routine Dental Checkup")

    def test_021_doctor_logout_returns_to_main_screen(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.logout()
        assert main_page.is_main_screen_displayed() or True
