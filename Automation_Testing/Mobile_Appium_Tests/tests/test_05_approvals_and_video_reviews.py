# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.doctor_login_page import DoctorLoginPage
from pages.doctor_dashboard_page import DoctorDashboardPage
from pages.pending_approvals_page import PendingApprovalsPage

@pytest.mark.doctor
class TestApprovalsAndVideoReviewsE2E:
    """E2E Test Suite for Doctor Approvals & Video Verification Reviews."""

    def test_018_approve_pending_patient_registration(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.open_pending_approvals()
        approvals_page = PendingApprovalsPage(driver)
        approvals_page.approve_first_user()

    def test_019_review_brushing_video_and_award_points(self, driver):
        main_page = MainPage(driver)
        main_page.click_doctor_role()
        doc_login = DoctorLoginPage(driver)
        doc_login.login_as_doctor("drsmith@example.com", "DocPass123!")
        doc_dashboard = DoctorDashboardPage(driver)
        doc_dashboard.open_video_reviews()
        reviews_page = PendingApprovalsPage(driver)
        reviews_page.play_review_video()
        reviews_page.award_video_points()
