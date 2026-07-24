import json
import os

MODULE_DISTRIBUTION = [
    ("Authentication", 40, "TC_AUTH_"),
    ("Authorization", 30, "TC_AUTHZ_"),
    ("Registration", 20, "TC_REG_"),
    ("Profile Management", 20, "TC_PROF_"),
    ("Navigation", 30, "TC_NAV_"),
    ("Dashboard", 20, "TC_DASH_"),
    ("Forms", 40, "TC_FORM_"),
    ("CRUD Operations", 40, "TC_CRUD_"),
    ("Search", 20, "TC_SRCH_"),
    ("Filters", 20, "TC_FLTR_"),
    ("Input Validation", 40, "TC_VAL_"),
    ("Error Handling", 20, "TC_ERR_"),
    ("Session Management", 20, "TC_SESS_"),
    ("Notifications", 20, "TC_NOTIF_"),
    ("File Upload", 20, "TC_UPLD_"),
    ("Offline Handling", 10, "TC_OFFL_"),
    ("Accessibility", 20, "TC_A11Y_"),
    ("Responsive UI", 10, "TC_RESP_"),
    ("Performance Smoke Tests", 20, "TC_PERF_"),
    ("Regression Suite", 50, "TC_REGRESS_")
]

PRIORITIES = ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"]

def build_test_cases():
    test_cases = []
    
    known_failures = {
        "TC_AUTH_010": ("OTP validation mismatch on invalid OTP resend", "AssertionError: OTP validation message expected 'Invalid OTP' but got 'Connection Timeout'"),
        "TC_FORM_008": ("Mandatory Field Validation missing red outline", "AssertionError: Required field border color should be #FF0000"),
        "TC_UPLD_002": ("Large File Upload memory limit exceeded", "AppiumException: Application crash detected during 50MB file transfer"),
        "TC_OFFL_005": ("Offline sync queue timeout", "TimeoutException: Cache queue sync did not complete within 10 seconds"),
        "TC_PERF_012": ("Cold start frame render latency > 500ms", "AssertionError: First meaningful paint took 680ms (Threshold: 500ms)"),
        "TC_VAL_018": ("Special character injection in address field", "ValidationError: Field failed SQL sanitization check"),
        "TC_REGRESS_035": ("Concurrent appointment booking race condition", "HTTP 409 Conflict: Slot already locked by another thread"),
        "TC_AUTHZ_015": ("Revoked token access check", "AssertionError: Access was granted with expired session token")
    }

    known_skips = {
        "TC_NOTIF_004": "Feature Disabled: Push notifications feature flag is turned off in test build",
        "TC_A11Y_019": "Hardware Dependent: TalkBack screen reader accessibility service not enabled on target emulator",
        "TC_RESP_008": "Device Specific: Foldable screen layout fold orientation API unavailable",
        "TC_UPLD_015": "External Dep: Cloud Storage S3 bucket mock server unreachable",
        "TC_CRUD_038": "Environment Issue: Sandbox DB cleanup routine pending"
    }

    for module_name, count, prefix in MODULE_DISTRIBUTION:
        for i in range(1, count + 1):
            tc_id = f"{prefix}{i:03d}"
            priority = PRIORITIES[(i - 1) % len(PRIORITIES)]
            
            test_name = f"Verify {module_name} functionality - Scenario {i}"
            preconditions = f"App launched, User navigate to {module_name} section."
            steps = f"1. Launch SmileApp\n2. Navigate to {module_name}\n3. Perform operation step {i}\n4. Verify expected state."
            test_data = f"module={module_name.lower().replace(' ', '_')}, param_id={i}"
            expected = f"{module_name} operation scenario {i} completes successfully and UI updates."
            
            if tc_id in known_failures:
                status = "FAILED"
                reason, stack = known_failures[tc_id]
                actual = f"FAILED: {reason}"
            elif tc_id in known_skips:
                status = "SKIPPED"
                reason = known_skips[tc_id]
                stack = f"Skipped: {reason}"
                actual = f"SKIPPED: {reason}"
            else:
                status = "PASSED"
                stack = ""
                actual = f"PASSED: {module_name} scenario {i} verified successfully."

            test_cases.append({
                "test_id": tc_id,
                "module": module_name,
                "test_name": test_name,
                "priority": priority,
                "preconditions": preconditions,
                "steps": steps,
                "test_data": test_data,
                "expected_result": expected,
                "actual_result": actual,
                "status": status,
                "failure_reason": stack if status == "FAILED" else "",
                "skip_reason": stack if status == "SKIPPED" else "",
                "duration_seconds": round(0.5 + (i * 0.17) % 3.5, 2)
            })

    return test_cases

if __name__ == "__main__":
    cases = build_test_cases()
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "test_data_400.json")
    with open(file_path, "w") as f:
        json.dump(cases, f, indent=2)
    print(f"Successfully generated {len(cases)} test cases in {file_path}")
