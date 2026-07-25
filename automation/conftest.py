import pytest
import time
import traceback
from automation.drivers.driver_factory import DriverFactory
from automation.utils.screenshot_util import ScreenshotUtil
from automation.utils.logger import logger

# Global container for collected execution results
GLOBAL_RESULTS = []

@pytest.fixture(scope="function")
def driver(request):
    driver_instance = DriverFactory.create_driver()
    yield driver_instance
    try:
        driver_instance.quit()
    except Exception:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        duration = round(report.duration, 3)
        test_name = item.name
        
        # Extract module name from class or module
        module_name = getattr(item.cls, "MODULE", "General") if item.cls else "General"
        test_id = item.name.split("[")[-1].replace("]", "") if "[" in item.name else item.name

        # Format ID clean if numerical
        if test_id.isdigit():
            if "Authentication" in module_name: test_id = f"TC_AUTH_{int(test_id):03d}"
            elif "Authorization" in module_name: test_id = f"TC_AZN_{int(test_id):03d}"
            elif "Navigation" in module_name: test_id = f"TC_NAV_{int(test_id):03d}"
            elif "UI Validation" in module_name: test_id = f"TC_UI_{int(test_id):03d}"
            elif "Forms" in module_name: test_id = f"TC_FORM_{int(test_id):03d}"
            elif "CRUD" in module_name: test_id = f"TC_CRUD_{int(test_id):03d}"
            elif "Input" in module_name: test_id = f"TC_INP_{int(test_id):03d}"
            elif "Error" in module_name: test_id = f"TC_ERR_{int(test_id):03d}"
            elif "Session" in module_name: test_id = f"TC_SES_{int(test_id):03d}"
            elif "File" in module_name: test_id = f"TC_UPL_{int(test_id):03d}"
            elif "Accessibility" in module_name: test_id = f"TC_ACC_{int(test_id):03d}"
            elif "Responsive" in module_name: test_id = f"TC_RSP_{int(test_id):03d}"
            elif "Performance" in module_name: test_id = f"TC_PRF_{int(test_id):03d}"
            elif "Regression" in module_name: test_id = f"TC_REG_{int(test_id):03d}"

        driver_inst = item.funcargs.get("driver", None)
        screenshot_path = ""
        failure_reason = ""
        stack_trace = ""

        if report.failed:
            status = "FAIL"
            failure_reason = str(report.longrepr)
            stack_trace = traceback.format_exc()
            if driver_inst:
                screenshot_path = ScreenshotUtil.capture_screenshot(driver_inst, test_id)
        elif report.skipped:
            status = "SKIP"
        else:
            status = "PASS"

        result_entry = {
            "id": test_id,
            "module": module_name,
            "name": test_name,
            "status": status,
            "duration": duration,
            "priority": "P1" if "AUTH" in test_id or "AZN" in test_id else "P2",
            "screenshot": screenshot_path,
            "failure_reason": failure_reason[:300] if failure_reason else "",
            "stack_trace": stack_trace[:500] if stack_trace else ""
        }
        GLOBAL_RESULTS.append(result_entry)
