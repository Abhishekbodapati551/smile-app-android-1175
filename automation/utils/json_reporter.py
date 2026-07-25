import json
from pathlib import Path
from typing import List, Dict
from automation.config.config import JSON_REPORTS_DIR
from automation.utils.logger import logger

class JSONReporter:
    @staticmethod
    def generate_report(results: List[Dict], total_duration: float):
        JSON_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        json_file = JSON_REPORTS_DIR / "execution-results.json"

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        skipped = sum(1 for r in results if r["status"] == "SKIP")
        pass_rate = round((passed / total * 100), 2) if total > 0 else 0.0

        payload = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "pass_rate_percentage": pass_rate,
                "duration_seconds": round(total_duration, 2),
                "quality_gate_passed": pass_rate >= 95.0
            },
            "test_cases": results
        }

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        logger.info(f"✓ Generated JSON report at {json_file}")
