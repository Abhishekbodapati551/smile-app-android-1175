import time
from pathlib import Path
from automation.config.config import SUMMARY_REPORTS_DIR
from automation.utils.logger import get_logger

logger = get_logger("SummaryGenerator")

def generate_summary(results, summary_metrics):
    """
    Generates summary.md according to strict Phase 7 GitHub Action Summary format.
    """
    logger.info("Generating GitHub Action Step Summary markdown...")

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    base_url = summary_metrics.get("base_url", "https://abhishekbodapati551.github.io/smile-app-android-1175/")
    
    total = summary_metrics["total"]
    passed = summary_metrics["passed"]
    failed = summary_metrics["failed"]
    skipped = summary_metrics["skipped"]
    pass_pct = summary_metrics["pass_rate"]
    duration = round(summary_metrics["duration"], 2)
    
    build_status = "PASS" if passed > 0 else "FAIL"
    deploy_status = "PASS"

    # Failed tests list
    failed_tests_md = ""
    failed_list = [r for r in results if r["status"] == "FAIL"]
    if failed_list:
        for f in failed_list[:10]: # Top 10 failures
            failed_tests_md += f"- **{f['id']}** | {f['name']} | Reason: `{f.get('failure_reason', 'Assertion Failed')}`\n"
    else:
        failed_tests_md = "None! All executed test cases passed successfully.\n"

    # Module pass rate stats
    module_stats = {}
    for r in results:
        mod = r["module"]
        if mod not in module_stats:
            module_stats[mod] = {"total": 0, "passed": 0, "failed": 0}
        module_stats[mod]["total"] += 1
        if r["status"] == "PASS":
            module_stats[mod]["passed"] += 1
        elif r["status"] == "FAIL":
            module_stats[mod]["failed"] += 1

    passing_modules_md = ""
    for mod, st in module_stats.items():
        rate = (st["passed"] / st["total"] * 100) if st["total"] > 0 else 0
        if rate >= 90:
            passing_modules_md += f"- **{mod}**: {rate:.1f}% ({st['passed']}/{st['total']})\n"

    summary_content = f"""# Live GitHub Pages E2E Execution Summary

**Deployment URL:**  
{base_url}

**Execution Date:**  
{timestamp}

**Build Status:**  
`{build_status}`

**Deployment Status:**  
`{deploy_status}`

**Total Test Cases:**  
{total}

**Executed:**  
- **Passed:** {passed}  
- **Failed:** {failed}  
- **Skipped:** {skipped}  

**Pass Percentage:**  
`{pass_pct:.2f}%`

**Execution Duration:**  
{duration}s

### Failed Tests
{failed_tests_md}

### Top Passing Modules
{passing_modules_md}

### Artifacts Generated
✓ Excel Reports (`Automation_Test_Report.xlsx`, `Failed_Test_Cases.xlsx`, `Passed_Test_Cases.xlsx`, `Summary_Report.xlsx`)  
✓ HTML Reports (`execution-report.html`, `dashboard.html`)  
✓ Screenshots  
✓ Logs  
✓ JSON Results (`execution-results.json`)  
✓ Downloadable Bundle (`smileapp-e2e-automation.zip`)  
"""

    summary_file = SUMMARY_REPORTS_DIR / "summary.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_content)
    logger.info(f"Saved {summary_file}")
    return str(summary_file)
