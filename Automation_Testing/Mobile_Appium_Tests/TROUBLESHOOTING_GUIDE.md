# Troubleshooting Guide - Android Appium E2E Automation

This guide documents common errors encountered during local execution and CI/CD runs, along with resolved remedies.

---

## 1. Appium Server Not Reachable (`WebDriverException: Connection Refused`)

### Cause
Appium server is not running on `http://127.0.0.1:4723/` or firewall is blocking loopback.

### Solution
1. Verify Appium is running:
   ```bash
   curl http://127.0.0.1:4723/status
   ```
2. Start Appium explicitly with `--cors` flag:
   ```bash
   appium --allow-cors
   ```

---

## 2. Emulator Boot Timeout in GitHub Actions

### Cause
Linux runner default nested virtualization might be slow for certain AVD architectures.

### Solution
- Use `macos-latest` runner or configure HAXM/KVM virtualization.
- Use `reactivecircus/android-emulator-runner@v2` with `target: google_apis` and `arch: x86_64`.

---

## 3. GitHub Pages Deployment Permission Denied (`403 Forbidden`)

### Cause
Workflow missing write permissions for contents or pages.

### Solution
Ensure `.github/workflows/android-e2e.yml` includes:
```yaml
permissions:
  contents: write
  pages: write
  id-token: write
```

---

## 4. Excel File Locking / Permission Errors

### Cause
Excel file `Automation_Test_Report.xlsx` is opened in Microsoft Excel while Python script tries to overwrite it.

### Solution
Close Microsoft Excel or run script to generate into `Test Results/Excel/` folder.
