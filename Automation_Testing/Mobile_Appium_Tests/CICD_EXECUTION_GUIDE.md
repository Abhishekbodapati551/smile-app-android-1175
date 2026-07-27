# CI/CD Execution Guide - GitHub Actions & GitHub Pages

This document outlines the complete 21-stage GitHub Actions execution flow and GitHub Pages hosting architecture for **SmileApp E2E Mobile Test Suite**.

---

## CI/CD Pipeline Workflow Architecture

The primary workflow is defined in [.github/workflows/android-e2e.yml](file:///.github/workflows/android-e2e.yml).

### Pipeline Stages Overview

1. **Stage 1: Checkout Repository** - Retrieves codebase with full history (`actions/checkout@v4`).
2. **Stage 2: Setup Java** - Configures OpenJDK 17 (`actions/setup-java@v4`).
3. **Stage 3: Setup Android SDK** - Initializes Android build tools and SDK targets.
4. **Stage 4: Install Dependencies** - Installs Python 3.11, Node.js 20, pytest, Appium, and openpyxl.
5. **Stage 5: Build APK** - Compiles `./gradlew assembleDebug`.
6. **Stage 6 & 7: Start Android Emulator & Verify Readiness** - Boots API 31 `x86_64` AVD headlessly and validates `boot_completed`.
7. **Stage 8: Install APK** - Executes `adb install -r` on the emulator.
8. **Stage 9 & 10: Start Appium Server & Verify Health** - Launches `appium` background process and tests HTTP health status (`/status`).
9. **Stage 11: Execute Appium E2E Tests** - Executes 400+ test cases via pytest runner.
10. **Stage 12 & 13: Screenshots & Device Logs** - Captures `adb logcat` logs and failure screenshots.
11. **Stage 14, 15, 16, 17: Generate Reports** - Invokes `generate_enterprise_reports.py` to create Excel, HTML, JSON, and Markdown summaries.
12. **Stage 18: Upload Artifacts** - Uploads all reports and `SmileApp_Android_Appium_E2E_Test_Artifacts.zip` (30 days retention).
13. **Stage 19 & 20: Publish Reports & Archive History** - Runs `scripts/publish_gh_pages.py` to update `reports/latest/` and archive into `reports/history/build-XXX/` on `gh-pages` branch.
14. **Stage 21: Publish GitHub Action Summary** - Writes `$GITHUB_STEP_SUMMARY` markdown overview.

---

## Live Report URL Format

Once deployed, access the interactive dashboard at:
`https://<github-username>.github.io/<repository-name>/reports/latest/execution-report.html`
