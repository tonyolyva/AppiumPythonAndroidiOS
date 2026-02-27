import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
import os
import datetime
import pytest_html
import base64

# Global variable to hold the driver instance (optional, but needed for the hook)
_driver_instance = None

# --- Fixture to provide capabilities for different platforms ---
# This fixture will be parameterized to yield different capability dictionaries.
# IMPORTANT: scope changed to "function"
@pytest.fixture(scope="function", params=[ # Changed scope to "function"
    # iOS Capabilities
    {
        "platform": "iOS",
        "app_path": "/Users/Yutaka/Library/Developer/Xcode/DerivedData/CalculMath-ezshmfewvjwlhqbluhlcdjdmhfvc/Build/Products/Debug-iphonesimulator/CalculMath.app",
        "deviceName": "iPhone 16 Pro Max",
        "platformVersion": "18.1",
        "appPackage": "com.example.CalculMath", # Optional: for consistency, can be set to bundle ID or app name
        "appActivity": "com.example.CalculMath.MainActivity" # Optional: for consistency
    },
    # Android Capabilities (Example - adjust appPackage/appActivity as needed)
    {
        "platform": "Android",
        "deviceName": "Pixel 3", # Example Android device name
        "platformVersion": "12",    # Example Android platform version
        "appPackage": "com.google.android.calculator",
        "appActivity": "com.android.calculator2.Calculator",
        "noReset": True
    }
], ids=["iOS_CalculMath", "Android_Calculator"]) # Add 'ids' for clearer test names
def appium_capabilities(request):
    """
    Provides Appium capabilities dictionaries for different platforms.
    """
    return request.param

# --- Fixture for Appium driver setup and teardown ---
# This fixture depends on 'appium_capabilities' to get the necessary parameters.
@pytest.fixture(scope="function")
def driver_setup(request, appium_capabilities): # <-- Now depends on 'appium_capabilities'
    global _driver_instance

    capabilities = appium_capabilities # Get the capabilities dictionary from the 'appium_capabilities' fixture
    
    platform = capabilities.get("platform")
    app_path = capabilities.get("app_path") # Specific for iOS
    
    appium_options = AppiumOptions()

    if platform == "Android":
        print(f"\n--- Setting up Android driver for {capabilities.get('deviceName')} on {capabilities.get('platformVersion')} ---")
        appium_options.load_capabilities({
            "platformName": capabilities.get("platform"),
            "appium:deviceName": capabilities.get("deviceName"),
            "appium:platformVersion": capabilities.get("platformVersion"),
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": capabilities.get("appPackage"),
            "appium:appActivity": capabilities.get("appActivity"),
            "appium:noReset": capabilities.get("noReset", False) # <--- CHANGE THIS LINE
            # The .get("noReset", False) ensures it defaults to False if not explicitly in capabilities,
            # but it will correctly pick up True if present.
        })
    elif platform == "iOS":
        # ... (rest of your iOS setup remains the same)
        print(f"\n--- Setting up iOS driver for {capabilities.get('deviceName')} on {capabilities.get('platformVersion')} ---")
        # Check if the app path exists before proceeding
        if not app_path or not os.path.exists(app_path):
            pytest.fail(f"CalculMath.app not found at {app_path}. Please update app_path in conftest.py or ensure the app exists at this location.")

        appium_options.load_capabilities({
            "platformName": capabilities.get("platform"),
            "appium:deviceName": capabilities.get("deviceName"),
            "appium:platformVersion": capabilities.get("platformVersion"),
            "appium:automationName": "XCUITest",
            "appium:app": app_path,
            "appium:noReset": False # Reset app state for each test
        })
    else:
        pytest.fail("Unsupported platform: " + platform)

    appium_server_url = 'http://localhost:4723'

    try:
        _driver_instance = webdriver.Remote(appium_server_url, options=appium_options)
        print("Successfully connected to Appium driver!")
    except Exception as e:
        print(f"Failed to connect to Appium driver: {e}")
        pytest.fail(f"Could not connect to Appium driver: {e}")

    yield _driver_instance # Provide the driver to the test function

    # Teardown: Quit the driver after each test function completes
    print("Tearing down Appium driver...")
    if _driver_instance:
        print("Quitting Appium driver session...")
        try:
            # --- ADD THIS LINE TO EXPLICITLY CLOSE THE APP ---
            _driver_instance.terminate_app(appium_capabilities.get("appPackage"))
            print(f"Terminated app: {appium_capabilities.get('appPackage')}")

            _driver_instance.quit()
            print("Session closed.")
        except Exception as e:
            print(f"Error during driver quit or app termination: {e}")
        _driver_instance = None

# Pytest hook to add screenshot to HTML report on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # print(f"\n--- Inside pytest_runtest_makereport for {report.nodeid}, when: {report.when} ---")

    driver = _driver_instance # Use the global driver instance
    # if driver:
    #     print(f"Driver in hook: {driver}")

    # print(f"Report outcome: {report.outcome}, Report when: {report.when}")

    # Only take screenshot if the test *failed* during the 'call' phase
    if report.when == 'call' and report.failed and driver: 
        print("Condition met for screenshot: report.when is 'call' and test is failed.")
        
        screenshot_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Sanitize nodeid for filename, replace invalid characters
        sanitized_nodeid = report.nodeid.replace(':', '_').replace('/', '_').replace('[', '_').replace(']', '').replace('.', '_')
        screenshot_filename = f"{sanitized_nodeid}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        
        full_screenshot_path = os.path.join(screenshot_dir, screenshot_filename) # Absolute path to save file

        try:
            driver.save_screenshot(full_screenshot_path)
            print(f"Screenshot saved to: {full_screenshot_path}")

            with open(full_screenshot_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            
            report.extras.append(pytest_html.extras.image(
                f"data:image/png;base64,{image_data}", 
                name=f"Screenshot on Failure: {report.nodeid}",
                mime_type='image/png'
            ))
            print("Screenshot data embedded into report.extra using pytest_html.extras.image.")
        except Exception as e:
            print(f"Failed to take screenshot or add to report: {e}")
    # else:
        # print(f"Screenshot condition NOT met: report.when={report.when}, report.failed={report.failed}, driver_present={bool(driver)}")


# Pytest hook for adding custom CSS to the HTML report
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        pytest_html.extras.html(
            '<style>'
            '  img.extra-image {'
            '    max-width: 100% !important;'
            '    height: auto !important;'
            '    display: block !important;'
            '    margin: 0 auto !important;'
            '    border: 1px solid #ddd;'
            '  }'
            '  details.extra-details {'
            '    width: 100%;'
            '    overflow-x: auto;'
            '    box-sizing: border-box;'
            '    margin-bottom: 10px;'
            '  }'
            '  .pytest-html-details-block {'
            '    max-width: 100%;'
            '    overflow-x: auto;'
            '  }'
            '  .pytest-html-container, .container-fluid {'
            '    max-width: 100% !important;'
            '    overflow-x: auto !important;'
            '  }'
            '</style>'
        )
    ])