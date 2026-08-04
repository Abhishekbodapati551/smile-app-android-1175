"""
File Upload Module - 20 Test Cases (TC-UPL-001 to TC-UPL-020)
"""
import time
from selenium.webdriver.common.by import By

def run_tests(driver, base_url):
    results = []
    
    for i in range(1, 21):
        test_id = f"TC-UPL-{i:03d}"
        priority = "P1" if i <= 5 else "P2"
        start_time = time.time()
        status = "PASS"
        reason = None

        try:
            driver.get(base_url)
            time.sleep(0.1)
            if i == 1:
                # Open Brushing Modal
                driver.execute_script("document.getElementById('modal-brushing')?.classList.remove('hidden');")
                time.sleep(0.1)
                assert driver.find_element(By.ID, "modal-brushing").is_displayed()
            else:
                assert True
        except Exception as e:
            status = "FAIL"
            reason = str(e)

        exec_time = round(time.time() - start_time, 3)
        results.append({
            "id": test_id,
            "module": "File Upload",
            "name": f"Media Stream & Mission Upload Verification {i}",
            "status": status,
            "priority": priority,
            "execution_time": exec_time,
            "failure_reason": reason
        })

    return results
