# Phase 7 — Live GitHub Pages E2E Selenium Automation Framework

Enterprise-grade QA Automation Framework & GitHub Actions CI/CD Pipeline executing 400+ Selenium test cases against live GitHub Pages deployments.

---

## 📁 Framework Structure

```
automation/
├── config/             # Environment, timeout, and BASE_URL configurations
├── drivers/            # Headless Chrome driver factory
├── pages/              # Page Object Models (POMs) for Smile App screens
├── tests/              # 400+ executable test cases across 14 modules
├── data/               # Test data generators and fixture models
├── utils/              # Reporting, logging, screenshot, verifier & zip utilities
├── reports/            # Output directory for Excel, HTML, JSON & Summary reports
├── screenshots/        # Failure screenshot evidence storage
├── logs/               # Execution log files
├── requirements.txt    # Python dependencies
├── run_tests.py        # Central test orchestrator and Quality Gate evaluator
└── README.md           # Documentation and execution guides
```

---

## 🛠️ Local Execution Guide

### Prerequisites
- Python 3.10+
- Google Chrome Browser (Latest stable)

### Step 1: Install Dependencies
```bash
pip install -r automation/requirements.txt
```

### Step 2: Set Target BASE_URL (Optional)
By default, tests execute against the live GitHub Pages URL. You can target any custom live deployment by setting `BASE_URL`:
```bash
export BASE_URL=https://<github-username>.github.io/<repository-name>/
```

### Step 3: Execute Test Suite & Generate Reports
```bash
python automation/run_tests.py
```

All 4 Excel reports, 2 HTML reports, JSON results, screenshots, summary markdown, and `smileapp-e2e-automation.zip` will be automatically generated in `automation/reports/` and project root.

---

## 🚀 CI/CD Execution Guide (GitHub Actions)

The pipeline automatically triggers on `push`, `pull_request`, and `workflow_dispatch` via `.github/workflows/deploy-and-test.yml`.

### Pipeline 13 Stages:
1. **Repository Checkout**: Clones latest repository commit.
2. **Dependency Installation**: Installs Python & dependencies from `automation/requirements.txt`.
3. **Build Application**: Static asset verification.
4. **Static Analysis**: Linting and HTML/JS verification.
5. **Deploy to GitHub Pages**: Publishes site to GitHub Pages.
6. **Wait for Deployment**: Polls live URL until deployment completes.
7. **Deployment Verification**: Asserts HTTP 200, CSS/JS load, and DOM elements.
8. **Run Selenium E2E Tests**: Executes 400+ Selenium tests in headless Chrome against live `BASE_URL`.
9. **Generate Reports**: HTML dashboard and execution reports.
10. **Generate Excel Reports**: Multi-sheet `.xlsx` workbooks.
11. **Upload Artifacts**: Archives Excel, HTML, screenshots, logs, JSON, and `.zip` for 30 days.
12. **Publish Summary**: Emits live status breakdown to `$GITHUB_STEP_SUMMARY`.
13. **Store Historical Results**: Retains execution metrics for trend analysis.

---

## ⚙️ Repository Configuration Guide

### 1. Enable GitHub Pages
1. Go to repository **Settings** -> **Pages**.
2. Set **Source** to **GitHub Actions**.

### 2. Configure Workflow Permissions
1. Go to repository **Settings** -> **Actions** -> **General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Check **Allow GitHub Actions to create and approve pull requests**.

### 3. Repository Variables (Optional)
- `BASE_URL`: `https://<github-username>.github.io/<repository-name>/`

---

## 🔍 Troubleshooting Guide

| Issue | Root Cause | Resolution |
| --- | --- | --- |
| `Deployment verification failed` | GitHub Pages site not yet published | Verify Pages is built in Settings -> Pages; wait 60s and retry. |
| `Chrome failed to start` | Missing Chrome dependencies in CI environment | Ensure `sudo apt-get install google-chrome-stable` ran in CI. |
| `Quality Gate Failed (<95%)` | >5% test cases failed | Inspect `automation/reports/Excel/Failed_Test_Cases.xlsx` or `dashboard.html`. |
| `Base URL Hardcode Error` | Hardcoded `http://localhost` used in tests | Ensure all test cases extend `BasePage` and fetch `BASE_URL`. |
