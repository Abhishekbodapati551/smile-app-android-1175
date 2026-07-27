import pytest
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import APPIUM_SERVER_URL, DESIRED_CAPS

@pytest.fixture(scope="session")
def driver_setup():
    """Session-level Appium driver fixture."""
    options = UiAutomator2Options()
    for key, value in DESIRED_CAPS.items():
        options.set_capability(key, value)

    try:
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        driver.implicitly_wait(5)
    except Exception as e:
        pytest.skip(f"Appium server not reachable at {APPIUM_SERVER_URL}. Error: {str(e)}")
        return None

    yield driver
    if driver:
        driver.quit()

@pytest.fixture(scope="function")
def driver(driver_setup):
    """Function-level driver fixture with app reset per test."""
    if not driver_setup:
        pytest.skip("Driver not initialized")
    driver_setup.activate_app(DESIRED_CAPS["appPackage"])
    yield driver_setup
    try:
        driver_setup.terminate_app(DESIRED_CAPS["appPackage"])
    except Exception:
        pass
