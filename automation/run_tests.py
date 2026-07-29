import sys
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from automation.config.config import BASE_URL, PASS_THRESHOLD_PERCENT
from automation.drivers.driver_factory import create_driver
from automation.utils.logger import get_logger
from automation.utils.screenshot import capture_screenshot
from automation.utils.excel_generator import generate_excel_reports
from automation.utils.report_generator import generate_reports
from automation.utils.summary_generator import generate_summary
from automation.utils.zip_archiver import archive_results

# Import test suites
from automation.tests import (
    test_authentication,
    test_authorization,
    test_navigation,
    test_ui_validation,
    test_forms,
    test_crud_operations,
    test_input_validation,
    test_error_handling,
    test_session_management,
    test_file_upload,
    test_accessibility,
    test_responsive_design,
    test_performance_smoke,
    test_regression
)

logger = get_logger("MasterTestRunner")

def run_all_tests():
    logger.info("====================================================")
    logger.info("STARTING LIVE SELENIUM E2E TEST SUITE EXECUTION")
    logger.info(f"Target BASE_URL: {BASE_URL}")
    logger.info(f"Required Pass Threshold: {PASS_THRESHOLD_PERCENT}%")
    logger.info("====================================================")

    start_total_time = time.time()
    all_results = []

    test_suites = [
        test_authentication,
        test_authorization,
        test_navigation,
        test_ui_validation,
        test_forms,
        test_crud_operations,
        test_input_validation,
        test_error_handling,
        test_session_management,
        test_file_upload,
        test_accessibility,
        test_responsive_design,
        test_performance_smoke,
        test_regression
    ]

    for suite in test_suites:
        module_name = suite.__name__.split('.')[-1]
        logger.info(f"Executing suite: {module_name}...")
        
        driver = None
        try:
            driver = create_driver(headless=True)
            suite_results = suite.run_tests(driver, BASE_URL)
            
            for res in suite_results:
                if res["status"] == "FAIL":
                    try:
                        shot_path = capture_screenshot(driver, res["id"], name=res["name"])
                        res["screenshot"] = shot_path
                    except Exception:
                        pass

            all_results.extend(suite_results)
        except Exception as e:
            logger.error(f"Error executing suite {module_name}: {e}")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    total_duration = time.time() - start_total_time
    total_tests = len(all_results)
    passed_tests = sum(1 for r in all_results if r["status"] == "PASS")
    failed_tests = sum(1 for r in all_results if r["status"] == "FAIL")
    skipped_tests = sum(1 for r in all_results if r["status"] == "SKIP")
    
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0.0

    summary_metrics = {
        "total": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "skipped": skipped_tests,
        "pass_rate": pass_rate,
        "duration": total_duration,
        "base_url": BASE_URL
    }

    logger.info("====================================================")
    logger.info("TEST EXECUTION COMPLETED")
    logger.info(f"Total: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests} | Skipped: {skipped_tests}")
    logger.info(f"Pass Rate: {pass_rate:.2f}% | Duration: {total_duration:.2f}s")
    logger.info("====================================================")

    # Generate all Excel Reports
    generate_excel_reports(all_results, summary_metrics)

    # Generate HTML & JSON Reports
    generate_reports(all_results, summary_metrics)

    # Generate Summary Markdown
    generate_summary(all_results, summary_metrics)

    # Archive into smileapp-e2e-automation.zip
    archive_results()

    # Pass/Fail Threshold Check
    if pass_rate < PASS_THRESHOLD_PERCENT:
        logger.error(f"FAIL: Pass rate {pass_rate:.2f}% is below required threshold of {PASS_THRESHOLD_PERCENT}%")
        sys.exit(1)
    else:
        logger.info(f"SUCCESS: Pass rate {pass_rate:.2f}% meets required threshold of {PASS_THRESHOLD_PERCENT}%")
        sys.exit(0)

if __name__ == "__main__":
    run_all_tests()
