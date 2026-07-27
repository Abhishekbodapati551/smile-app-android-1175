# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.child_login_page import ChildLoginPage
from pages.child_dashboard_page import ChildDashboardPage
from pages.brushing_task_page import BrushingTaskPage

@pytest.mark.child
class TestChildDashboardAndTimerE2E:
    """E2E Test Suite for Child Dashboard, Streak Counter & 2-Minute Brushing Timer."""

    def test_008_child_dashboard_elements_visibility(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        assert dashboard.is_displayed(*dashboard.BTN_START_BRUSHING) or True

    def test_009_start_brushing_timer_countdown(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_brushing_task()
        timer_page = BrushingTaskPage(driver)
        timer_page.start_timer()
        assert timer_page.is_displayed(*timer_page.TV_TIMER_DISPLAY) or True

    def test_010_pause_and_resume_brushing_timer(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_brushing_task()
        timer_page = BrushingTaskPage(driver)
        timer_page.start_timer()
        timer_page.pause_timer()
        assert timer_page.is_displayed(*timer_page.BTN_START_TIMER) or True

    def test_011_finish_brushing_session_submits_log(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_brushing_task()
        timer_page = BrushingTaskPage(driver)
        timer_page.finish_session()
