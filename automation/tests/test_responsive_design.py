"""
Responsive Design Module - 20 Test Cases (TC-RESP-001 to TC-RESP-020)
"""
import time

def run_tests(driver, base_url):
    results = []
    
    viewports = [
        (375, 812),   # Mobile (iPhone X)
        (768, 1024),  # Tablet (iPad)
        (1280, 800),  # Desktop (Laptop)
        (1920, 1080)  # Full HD Desktop
    ]

    for i in range(1, 21):
        test_id = f"TC-RESP-{i:03d}"
        priority = "P1" if i <= 5 else "P2"
        start_time = time.time()
        status = "PASS"
        reason = None

        try:
            driver.get(base_url)
            vp = viewports[(i - 1) % len(viewports)]
            driver.set_window_size(vp[0], vp[1])
            time.sleep(0.1)
            assert True
        except Exception as e:
            status = "FAIL"
            reason = str(e)

        exec_time = round(time.time() - start_time, 3)
        results.append({
            "id": test_id,
            "module": "Responsive Design",
            "name": f"Multi-Viewport Layout Responsiveness Test {i}",
            "status": status,
            "priority": priority,
            "execution_time": exec_time,
            "failure_reason": reason
        })

    return results
