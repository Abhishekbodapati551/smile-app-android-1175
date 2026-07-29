import json
import time
from pathlib import Path
from automation.config.config import HTML_REPORTS_DIR, JSON_REPORTS_DIR
from automation.utils.logger import get_logger

logger = get_logger("ReportGenerator")

def generate_reports(results, summary_metrics):
    """
    Generates:
    1. HTML/execution-report.html
    2. HTML/dashboard.html
    3. JSON/execution-results.json
    """
    logger.info("Generating HTML and JSON reports...")

    # 1. JSON Report
    json_path = JSON_REPORTS_DIR / "execution-results.json"
    json_data = {
        "metrics": summary_metrics,
        "results": results
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"Saved {json_path}")

    # Helper html template builder
    passed_pct = summary_metrics["pass_rate"]
    failed_cnt = summary_metrics["failed"]
    passed_cnt = summary_metrics["passed"]
    skipped_cnt = summary_metrics["skipped"]
    total_cnt = summary_metrics["total"]
    duration_sec = round(summary_metrics["duration"], 2)
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Group by module for trend/module summary
    module_stats = {}
    for r in results:
        mod = r["module"]
        if mod not in module_stats:
            module_stats[mod] = {"total": 0, "pass": 0, "fail": 0, "skip": 0}
        module_stats[mod]["total"] += 1
        if r["status"] == "PASS":
            module_stats[mod]["pass"] += 1
        elif r["status"] == "FAIL":
            module_stats[mod]["fail"] += 1
        else:
            module_stats[mod]["skip"] += 1

    # 2. HTML/execution-report.html
    rows_html = ""
    for r in results:
        status_cls = "bg-green-100 text-green-800" if r["status"] == "PASS" else ("bg-red-100 text-red-800" if r["status"] == "FAIL" else "bg-yellow-100 text-yellow-800")
        reason = f"<div class='text-xs text-red-600 font-mono mt-1'>{r.get('failure_reason', '')}</div>" if r.get('failure_reason') else ""
        screenshot_link = f"<a href='../../{r.get('screenshot')}' target='_blank' class='text-blue-500 underline text-xs'>View Image</a>" if r.get('screenshot') else "-"
        rows_html += f"""
        <tr class="border-b hover:bg-slate-50">
            <td class="p-3 text-xs font-bold font-mono text-slate-700">{r['id']}</td>
            <td class="p-3 text-xs font-semibold text-slate-600">{r['module']}</td>
            <td class="p-3 text-xs font-bold text-slate-800">{r['name']}{reason}</td>
            <td class="p-3 text-xs"><span class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase {status_cls}">{r['status']}</span></td>
            <td class="p-3 text-xs text-slate-500 font-mono">{r.get('execution_time', 0.05)}s</td>
            <td class="p-3 text-xs font-bold text-slate-500">{r.get('priority', 'P2')}</td>
            <td class="p-3 text-xs">{screenshot_link}</td>
        </tr>
        """

    html_report_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmileApp - Selenium Execution Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 font-sans p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <div class="bg-slate-900 text-white p-8 rounded-3xl shadow-xl flex justify-between items-center">
            <div>
                <h1 class="text-3xl font-black">SmileApp Live E2E Automation Report</h1>
                <p class="text-slate-400 text-sm mt-1">Target URL: <span class="text-teal-400 font-mono">{summary_metrics.get('base_url')}</span></p>
            </div>
            <div class="text-right">
                <div class="text-xs uppercase tracking-widest text-slate-400">Timestamp</div>
                <div class="text-sm font-bold font-mono text-teal-300">{timestamp_str}</div>
            </div>
        </div>

        <!-- Metrics Cards -->
        <div class="grid grid-cols-2 md:grid-cols-6 gap-4">
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Total Tests</p>
                <p class="text-3xl font-black text-slate-800">{total_cnt}</p>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Passed</p>
                <p class="text-3xl font-black text-green-600">{passed_cnt}</p>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Failed</p>
                <p class="text-3xl font-black text-red-600">{failed_cnt}</p>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Skipped</p>
                <p class="text-3xl font-black text-yellow-600">{skipped_cnt}</p>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Pass Rate</p>
                <p class="text-3xl font-black text-blue-600">{passed_pct:.1f}%</p>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow border border-slate-200">
                <p class="text-xs font-bold text-slate-400 uppercase">Duration</p>
                <p class="text-3xl font-black text-purple-600">{duration_sec}s</p>
            </div>
        </div>

        <!-- Executed Cases Table -->
        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200">
            <div class="p-6 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
                <h2 class="text-xl font-black text-slate-800">Test Execution Details ({total_cnt} Cases)</h2>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-100 text-slate-600 uppercase text-[10px] tracking-wider border-b">
                            <th class="p-3">Test ID</th>
                            <th class="p-3">Module</th>
                            <th class="p-3">Test Name</th>
                            <th class="p-3">Status</th>
                            <th class="p-3">Duration</th>
                            <th class="p-3">Priority</th>
                            <th class="p-3">Screenshot</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""
    exec_report_path = HTML_REPORTS_DIR / "execution-report.html"
    with open(exec_report_path, "w", encoding="utf-8") as f:
        f.write(html_report_content)
    logger.info(f"Saved {exec_report_path}")

    # 3. HTML/dashboard.html
    module_rows_html = ""
    for mod, st in module_stats.items():
        m_pass_rate = (st["pass"] / st["total"] * 100) if st["total"] > 0 else 0
        module_rows_html += f"""
        <div class="bg-white p-4 rounded-2xl shadow border border-slate-200 flex justify-between items-center">
            <div>
                <p class="font-bold text-slate-800 text-sm">{mod}</p>
                <p class="text-xs text-slate-400">{st['pass']}/{st['total']} Passed ({m_pass_rate:.1f}%)</p>
            </div>
            <div class="w-32 bg-slate-100 rounded-full h-3 overflow-hidden">
                <div class="bg-green-500 h-full" style="width: {m_pass_rate}%"></div>
            </div>
        </div>
        """

    dashboard_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmileApp - Automation Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 font-sans p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <div class="flex justify-between items-center bg-blue-600 text-white p-8 rounded-3xl shadow-lg">
            <div>
                <h1 class="text-3xl font-black">Executive Quality Dashboard</h1>
                <p class="text-blue-100 text-sm mt-1">Live E2E Continuous Integration Pipeline Status</p>
            </div>
            <div class="bg-white text-blue-900 px-6 py-3 rounded-2xl font-black text-2xl shadow">
                {passed_pct:.1f}% PASS
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-3xl shadow border border-slate-200">
                <h2 class="text-lg font-black text-slate-800 mb-4">Module Breakdown</h2>
                <div class="space-y-3">
                    {module_rows_html}
                </div>
            </div>
            
            <div class="bg-white p-6 rounded-3xl shadow border border-slate-200 space-y-4">
                <h2 class="text-lg font-black text-slate-800">Pipeline Execution Summary</h2>
                <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200 text-sm space-y-2">
                    <p><strong>Deployment URL:</strong> {summary_metrics.get('base_url')}</p>
                    <p><strong>Execution Status:</strong> <span class="text-green-600 font-bold">COMPLETED</span></p>
                    <p><strong>Total Executed Cases:</strong> {total_cnt}</p>
                    <p><strong>Passed:</strong> {passed_cnt}</p>
                    <p><strong>Failed:</strong> {failed_cnt}</p>
                    <p><strong>Skipped:</strong> {skipped_cnt}</p>
                </div>
                <div class="pt-4">
                    <a href="execution-report.html" class="block w-full text-center bg-slate-900 text-white py-4 rounded-2xl font-black hover:bg-slate-800 transition">View Detailed Execution Report</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    dashboard_path = HTML_REPORTS_DIR / "dashboard.html"
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_content)
    logger.info(f"Saved {dashboard_path}")
