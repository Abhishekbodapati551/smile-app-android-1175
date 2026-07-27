import os

# Appium Server Configuration
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")

# Android Device & Application Capabilities
DESIRED_CAPS = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
    "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", "13.0"),
    "appPackage": "com.example.smileapp",
    "appActivity": ".MainActivity",
    "noReset": False,
    "fullReset": False,
    "autoGrantPermissions": True,
    "newCommandTimeout": 300
}

# Test Run Settings
DEFAULT_TIMEOUT = 15
EXPLICIT_WAIT_TIMEOUT = 10
IMPLICIT_WAIT_TIMEOUT = 5

# Report Output Settings
REPORT_OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_REPORT_NAME = "SmileApp_E2E_Test_Report.xlsx"
EXCEL_REPORT_PATH = os.path.join(REPORT_OUTPUT_DIR, EXCEL_REPORT_NAME)
