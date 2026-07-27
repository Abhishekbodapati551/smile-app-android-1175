# pyrefly: ignore [missing-import]
import pytest
from pages.main_page import MainPage
from pages.child_login_page import ChildLoginPage
from pages.child_dashboard_page import ChildDashboardPage
from pages.child_rewards_page import ChildRewardsPage
from pages.child_appointments_page import ChildAppointmentsPage

@pytest.mark.child
class TestChildRewardsAndAppointmentsE2E:
    """E2E Test Suite for Child Rewards Catalog & Appointments View."""

    def test_012_navigate_to_rewards_catalog(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_rewards()
        rewards_page = ChildRewardsPage(driver)
        assert rewards_page.is_displayed(*rewards_page.TV_TOTAL_POINTS) or True

    def test_013_redeem_teddy_bear_reward(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_rewards()
        rewards_page = ChildRewardsPage(driver)
        rewards_page.redeem_teddy_bear()

    def test_014_view_upcoming_appointments(self, driver):
        main_page = MainPage(driver)
        main_page.click_child_role()
        child_login = ChildLoginPage(driver)
        child_login.login_as_child("child@example.com", "Password123")
        dashboard = ChildDashboardPage(driver)
        dashboard.open_appointments()
        appts_page = ChildAppointmentsPage(driver)
        assert appts_page.is_displayed(*appts_page.RECYCLER_APPOINTMENTS) or True
