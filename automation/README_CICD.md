# CI/CD Execution Guide - GitHub Actions

## Overview
Phase 7 CI/CD pipeline deploys the application to GitHub Pages on every code push or pull request, verifies the live deployment availability, executes 440 Selenium E2E test cases in headless Chrome, generates Excel and HTML reports, archives evidence into a downloadable ZIP file, and publishes summaries.

## Workflow File
`.github/workflows/deploy-and-test.yml`

## GitHub Repository Requirements

### 1. Enable GitHub Pages
- Go to Repository Settings -> Pages.
- Source: Set to **GitHub Actions**.

### 2. Workflow Permissions
- Ensured in workflow file:
  - `contents: read`
  - `pages: write`
  - `id-token: write`

### 3. Pipeline Stages
1. **Stage 1**: Repository Checkout
2. **Stage 2**: Set up Python & Install Automation Dependencies
3. **Stage 3**: Build Application Assets
4. **Stage 4**: Static Analysis & HTML Linting
5. **Stage 5**: Deploy Application to GitHub Pages (`actions/deploy-pages@v4`)
6. **Stage 6**: Wait for Deployment Propagation (15s)
7. **Stage 7**: Deployment Verification (HTTP 200 GET check)
8. **Stage 8**: Execute Headless Selenium E2E Test Suite (400+ Test Cases)
9. **Stage 9**: Generate Multi-Format Reports & JSON Results
10. **Stage 10**: Generate Styled Multi-Tab Excel Reports
11. **Stage 11**: Upload Artifacts (`smileapp-e2e-automation-reports`)
12. **Stage 12**: Publish Summary (`$GITHUB_STEP_SUMMARY`)
13. **Stage 13**: Store Historical Execution Results

## Downloading Results
In GitHub Actions:
1. Go to the **Actions** tab.
2. Select the latest run of **Phase 7 - Complete CI/CD Deployment & Live E2E Testing**.
3. Scroll down to **Artifacts**.
4. Download `smileapp-e2e-automation-reports.zip`, which contains `smileapp-e2e-automation.zip`, Excel reports, HTML dashboards, logs, and screenshots.
