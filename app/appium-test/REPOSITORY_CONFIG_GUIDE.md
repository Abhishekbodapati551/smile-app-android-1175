# Repository Configuration Guide - GitHub Pages & Action Settings

To ensure automatic deployment of E2E test reports to GitHub Pages on every push, follow these repository configuration steps.

---

## 1. Enable GitHub Pages

1. Navigate to your repository on GitHub: `https://github.com/<username>/<repo>`
2. Go to **Settings** -> **Pages** (under Code and automation).
3. Under **Build and deployment**:
   - **Source**: Select `Deploy from a branch` or `GitHub Actions`.
   - **Branch**: Select `gh-pages` branch, `/ (root)` folder, and click **Save**.

---

## 2. Configure Workflow Permissions

1. Go to **Settings** -> **Actions** -> **General**.
2. Scroll to **Workflow permissions**.
3. Select **Read and write permissions**.
4. Check **Allow GitHub Actions to create and approve pull requests**.
5. Click **Save**.

---

## 3. Accessing Test Reports & Downloadable ZIP

Once the workflow finishes, reports will be hosted at:
- **Interactive Execution Report:** `https://<username>.github.io/<repo>/reports/latest/execution-report.html`
- **Executive Dashboard:** `https://<username>.github.io/<repo>/reports/latest/dashboard.html`
- **Historical Trends:** `https://<username>.github.io/<repo>/reports/latest/trends.html`
- **Downloadable ZIP Artifact Pack:** `https://<username>.github.io/<repo>/reports/latest/SmileApp_Android_Appium_E2E_Test_Artifacts.zip`

In addition, you can download `SmileApp_Android_Appium_E2E_Test_Artifacts.zip` directly from the **Summary** tab of any GitHub Action run!
