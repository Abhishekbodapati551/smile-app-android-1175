import sys
import time
import pytest
from pathlib import Path
from automation.config.config import AUTOMATION_ROOT, PASS_THRESHOLD_PERCENT, BASE_URL
from automation.utils.logger import logger
from automation.utils.deployment_verifier import DeploymentVerifier
from automation.utils.excel_reporter import ExcelReporter
from automation.utils.html_reporter import HTMLReporter
from automation.utils.json_reporter import JSONReporter
from automation.utils.summary_reporter import SummaryReporter
from automation.utils.zip_generator import ZipGenerator
from automation.conftest import GLOBAL_RESULTS

def run_all():
    logger.info("====================================================")
    logger.info("PHASE 7 — LIVE GITHUB PAGES E2E AUTOMATION EXECUTION")
    logger.info("====================================================")
    logger.info(f"Target BASE_URL: {BASE_URL}")

    # Stage 7: Deployment Verification
    deploy_ok = DeploymentVerifier.verify_deployment(BASE_URL)
    if not deploy_ok:
        logger.error("❌ Live Deployment Verification Failed! Aborting E2E Execution.")
        sys.exit(1)

    # Stage 8: Run Selenium E2E Tests
    t0 = time.time()
    tests_path = str(AUTOMATION_ROOT / "tests")
    pytest_args = [
        tests_path,
        "-v",
        "--tb=short"
    ]
    logger.info("Executing 400+ Selenium E2E Test Cases...")
    pytest.main(pytest_args)
    total_duration = time.time() - t0

    results = list(GLOBAL_RESULTS)
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["status"] == "PASS")
    failed_tests = sum(1 for r in results if r["status"] == "FAIL")
    skipped_tests = sum(1 for r in results if r["status"] == "SKIP")
    pass_rate = round((passed_tests / total_tests * 100), 2) if total_tests > 0 else 0.0

    logger.info("====================================================")
    logger.info(f"Execution Summary: Total={total_tests}, Passed={passed_tests}, Failed={failed_tests}, Skipped={skipped_tests}")
    logger.info(f"Pass Rate: {pass_rate}% (Target Gate: ≥{PASS_THRESHOLD_PERCENT}%)")
    logger.info("====================================================")

    # Stages 9 & 10: Generate Reports
    logger.info("Generating Excel, HTML, JSON & Summary Reports...")
    ExcelReporter.create_reports(results)
    HTMLReporter.generate_reports(results, total_duration)
    JSONReporter.generate_report(results, total_duration)
    SummaryReporter.generate_markdown_summary(results, total_duration)

    # ZIP Bundle Packaging
    ZipGenerator.create_automation_zip()

    # Pass / Fail Quality Gate logic
    if pass_rate >= PASS_THRESHOLD_PERCENT:
        logger.info("✓ QUALITY GATE PASSED!")
        sys.exit(0)
    else:
        logger.error(f"❌ QUALITY GATE FAILED! Pass rate {pass_rate}% is below threshold {PASS_THRESHOLD_PERCENT}%")
        sys.exit(1)

if __name__ == "__main__":
    run_all()
