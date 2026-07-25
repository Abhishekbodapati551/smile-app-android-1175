import time
from pathlib import Path
from typing import List, Dict
from automation.config.config import SUMMARY_REPORTS_DIR, BASE_URL
from automation.utils.logger import logger

class SummaryReporter:
    @staticmethod
    def generate_markdown_summary(results: List[Dict], total_duration: float, build_status="PASS", deploy_status="PASS") -> str:
        SUMMARY_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        summary_file = SUMMARY_REPORTS_DIR / "summary.md"

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIP")
        pass_rate = round((passed / total * 100), 2) if total > 0 else 0.0

        # Module aggregation
        module_stats = {}
        for r in results:
            mod = r.get("module", "General")
            if mod not in module_stats:
                module_stats[mod] = {"total": 0, "passed": 0, "failed": 0}
            module_stats[mod]["total"] += 1
            if r["status"] == "PASS":
                module_stats[mod]["passed"] += 1
            elif r["status"] == "FAIL":
                module_stats[mod]["failed"] += 1

        top_passing = []
        for mod, stats in module_stats.items():
            rate = round((stats["passed"] / stats["total"] * 100), 1) if stats["total"] > 0 else 0.0
            top_passing.append((mod, rate, stats["passed"], stats["total"]))
        top_passing.sort(key=lambda x: x[1], reverse=True)

        failed_tests = [r for r in results if r["status"] == "FAIL"]

        md_content = f"""# Live GitHub Pages E2E Execution Summary

**Deployment URL:**
[{BASE_URL}]({BASE_URL})

**Execution Date:**
{time.strftime("%Y-%m-%d %H:%M:%S UTC")}

**Build Status:**
`{build_status}`

**Deployment Status:**
`{deploy_status}`

**Total Test Cases:**
`{total}`

| Metric | Value |
| --- | --- |
| **Executed** | {total} |
| **Passed** | {passed} |
| **Failed** | {failed} |
| **Skipped** | {skipped} |
| **Pass Percentage** | **{pass_rate}%** |
| **Execution Duration** | {round(total_duration, 2)}s |

---

### Top Passing Modules

| Module Name | Pass Rate | Passed / Total |
| --- | --- | --- |
"""
        for mod, rate, p_cnt, t_cnt in top_passing[:10]:
            md_content += f"| **{mod}** | {rate}% | {p_cnt} / {t_cnt} |\n"

        if failed_tests:
            md_content += """
---

### Failed Tests

| Test ID | Test Name | Failure Reason |
| --- | --- | --- |
"""
            for ft in failed_tests[:15]:
                md_content += f"| `{ft.get('id')}` | {ft.get('name')} | {ft.get('failure_reason', 'Assertion Failed')} |\n"

        md_content += """
---

### Artifacts Generated

- ✓ Excel Reports (`Automation_Test_Report.xlsx`, `Failed_Test_Cases.xlsx`, `Passed_Test_Cases.xlsx`, `Summary_Report.xlsx`)
- ✓ HTML Reports (`execution-report.html`, `dashboard.html`)
- ✓ Failure Screenshots & Browser Logs
- ✓ JSON Results (`execution-results.json`)
- ✓ Complete ZIP Bundle (`smileapp-e2e-automation.zip`)
"""

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"✓ Generated summary.md at {summary_file}")
        return md_content
