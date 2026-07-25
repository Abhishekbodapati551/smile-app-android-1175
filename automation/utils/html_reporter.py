import json
import time
from pathlib import Path
from typing import List, Dict
from automation.config.config import HTML_REPORTS_DIR, BASE_URL
from automation.utils.logger import logger

class HTMLReporter:
    @staticmethod
    def generate_reports(results: List[Dict], total_duration: float):
        HTML_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        exec_report = HTML_REPORTS_DIR / "execution-report.html"
        dashboard_report = HTML_REPORTS_DIR / "dashboard.html"

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIP")
        pass_rate = round((passed / total * 100), 2) if total > 0 else 0.0

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smile App - Live E2E Automation Execution Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Outfit', sans-serif; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }}
    </style>
</head>
<body class="p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <div class="card p-6 rounded-3xl flex justify-between items-center">
            <div>
                <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-teal-300">
                    Live GitHub Pages E2E Execution Report
                </h1>
                <p class="text-slate-400 text-sm mt-1">Deployment URL: <a href="{BASE_URL}" target="_blank" class="text-blue-400 underline">{BASE_URL}</a></p>
                <p class="text-slate-400 text-xs mt-1">Timestamp: {time.strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
            </div>
            <div class="text-right">
                <span class="inline-block px-4 py-2 rounded-full font-bold text-sm {'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' if pass_rate >= 95.0 else 'bg-rose-500/20 text-rose-400 border border-rose-500/40'}">
                    Quality Gate: {'PASSED (≥95%)' if pass_rate >= 95.0 else 'FAILED (<95%)'}
                </span>
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="card p-5 rounded-2xl text-center">
                <p class="text-slate-400 text-xs font-semibold uppercase tracking-wider">Total Tests</p>
                <p class="text-3xl font-black text-white mt-1">{total}</p>
            </div>
            <div class="card p-5 rounded-2xl text-center">
                <p class="text-slate-400 text-xs font-semibold uppercase tracking-wider">Passed</p>
                <p class="text-3xl font-black text-emerald-400 mt-1">{passed}</p>
            </div>
            <div class="card p-5 rounded-2xl text-center">
                <p class="text-slate-400 text-xs font-semibold uppercase tracking-wider">Failed</p>
                <p class="text-3xl font-black text-rose-400 mt-1">{failed}</p>
            </div>
            <div class="card p-5 rounded-2xl text-center">
                <p class="text-slate-400 text-xs font-semibold uppercase tracking-wider">Skipped</p>
                <p class="text-3xl font-black text-amber-400 mt-1">{skipped}</p>
            </div>
            <div class="card p-5 rounded-2xl text-center">
                <p class="text-slate-400 text-xs font-semibold uppercase tracking-wider">Pass Rate</p>
                <p class="text-3xl font-black text-blue-400 mt-1">{pass_rate}%</p>
            </div>
        </div>

        <!-- Chart Section -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="card p-6 rounded-3xl">
                <h3 class="text-lg font-bold text-slate-200 mb-4">Test Execution Breakdown</h3>
                <div class="w-64 h-64 mx-auto">
                    <canvas id="chartStatus"></canvas>
                </div>
            </div>
            <div class="card p-6 rounded-3xl">
                <h3 class="text-lg font-bold text-slate-200 mb-4">Execution Summary Info</h3>
                <div class="space-y-3 text-sm">
                    <div class="flex justify-between border-b border-slate-700/50 pb-2">
                        <span class="text-slate-400">Total Duration:</span>
                        <span class="font-semibold text-white">{round(total_duration, 2)} seconds</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700/50 pb-2">
                        <span class="text-slate-400">Target Pass Threshold:</span>
                        <span class="font-semibold text-white">95.0%</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700/50 pb-2">
                        <span class="text-slate-400">Headless Chrome Version:</span>
                        <span class="font-semibold text-white">Latest Stable</span>
                    </div>
                    <div class="flex justify-between border-b border-slate-700/50 pb-2">
                        <span class="text-slate-400">Framework:</span>
                        <span class="font-semibold text-white">Selenium WebDriver + Python</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Test Results Table -->
        <div class="card p-6 rounded-3xl">
            <h3 class="text-lg font-bold text-slate-200 mb-4">Test Cases Execution Log ({total} Total)</h3>
            <div class="overflow-x-auto max-h-[500px]">
                <table class="w-full text-left text-xs">
                    <thead class="bg-slate-800 text-slate-400 uppercase sticky top-0">
                        <tr>
                            <th class="p-3">Test ID</th>
                            <th class="p-3">Module</th>
                            <th class="p-3">Test Name</th>
                            <th class="p-3">Priority</th>
                            <th class="p-3">Status</th>
                            <th class="p-3">Time (s)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
"""
        for t in results:
            status = t.get("status", "PASS")
            badge_cls = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" if status == "PASS" else ("bg-rose-500/20 text-rose-400 border border-rose-500/30" if status == "FAIL" else "bg-amber-500/20 text-amber-400 border border-amber-500/30")
            html_content += f"""
                        <tr class="hover:bg-slate-800/50">
                            <td class="p-3 font-mono text-blue-300">{t.get('id')}</td>
                            <td class="p-3 font-semibold text-slate-300">{t.get('module')}</td>
                            <td class="p-3 text-slate-200">{t.get('name')}</td>
                            <td class="p-3 text-slate-400">{t.get('priority')}</td>
                            <td class="p-3"><span class="px-2.5 py-1 rounded-full font-bold text-[10px] {badge_cls}">{status}</span></td>
                            <td class="p-3 text-slate-400">{t.get('duration', 0.0)}s</td>
                        </tr>
"""
        html_content += f"""
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('chartStatus').getContext('2d');
        new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Passed', 'Failed', 'Skipped'],
                datasets: [{{
                    data: [{passed}, {failed}, {skipped}],
                    backgroundColor: ['#10b981', '#f43f5e', '#f59e0b'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        with open(exec_report, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(dashboard_report, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info("✓ Generated HTML execution report & dashboard successfully.")
