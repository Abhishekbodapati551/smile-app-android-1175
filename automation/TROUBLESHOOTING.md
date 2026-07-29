# Troubleshooting Guide - Phase 7 E2E Automation

## Common Issues & Diagnostics

### 1. Deployment Verification Failure (HTTP Status != 200)
- **Symptom**: Stage 7 fails with `Deployment Verification Failed`.
- **Cause**: GitHub Pages DNS propagation delay or repository Pages configuration disabled.
- **Solution**: Check repository Settings -> Pages. Ensure source is set to `GitHub Actions`.

### 2. Selenium WebDriver Chrome Exception
- **Symptom**: `selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary`
- **Cause**: Chrome browser not installed or missing `--no-sandbox` flags.
- **Solution**: Ensure Chrome is installed and `automation/drivers/driver_factory.py` includes `--no-sandbox` and `--headless=new`.

### 3. OpenPyXL Module Not Found
- **Symptom**: `ModuleNotFoundError: No module named 'openpyxl'`
- **Cause**: Missing Python dependencies.
- **Solution**: Run `pip install -r automation/requirements.txt`.

### 4. Workflow Fails Pass Threshold
- **Symptom**: Workflow fails at Stage 8 with `Pass rate is below required threshold of 95.0%`.
- **Cause**: More than 5% of critical test cases failed.
- **Solution**: Check `automation/reports/HTML/execution-report.html` and `automation/screenshots/` to inspect failure tracebacks.
