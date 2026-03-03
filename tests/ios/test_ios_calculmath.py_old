import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy

def test_ios_calculmath_add_pos_result(driver_setup, appium_capabilities):
    # This check happens at runtime, after appium_capabilities has been resolved
    if appium_capabilities["platform"] != "iOS":
        pytest.skip("Skipping iOS test as current capabilities are not for iOS.")

    driver = driver_setup # The driver is provided by the fixture
    
    print("Performing calculation: 3 + 2 = 5 on CalculMath (iOS)")
    
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '3').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '+').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '2').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '=').click()
    
    # time.sleep(1) # Keep the app open for a bit for observation
    
    result_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'displayValue')
    actual_result = result_element.text
    # print(f"================ iOS add pos res. actual_result: {actual_result} ==============")

    expected_result = "5" 
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"

def test_ios_calculmath_mul_pos_result(driver_setup, appium_capabilities):
        # This check happens at runtime, after appium_capabilities has been resolved
    if appium_capabilities["platform"] != "iOS":
        pytest.skip("Skipping iOS test as current capabilities are not for iOS.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 3 * 2 = 6 on CalculMath (iOS)")

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '3').click()
    # time.sleep(2)
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '*').click()
    # time.sleep(2)
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '2').click()
    # time.sleep(2)
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '=').click()
    # time.sleep(2)

    result_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'displayValue')
    actual_result = result_element.text
    # print(f"================ iOS mul pos res. actual_result: {actual_result} ==============")
    # time.sleep(2)
    expected_result = "6" 
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"

def test_ios_calculmath_sub_pos_result(driver_setup, appium_capabilities):
    # This check happens at runtime, after appium_capabilities has been resolved
    if appium_capabilities["platform"] != "iOS":
        pytest.skip("Skipping iOS test as current capabilities are not for iOS.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 3 - 2 = 1 on CalculMath (iOS)")

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '3').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '-').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '2').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '=').click()

    result_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'displayValue')
    actual_result = result_element.text
    print(f"================ iOS sub pos res. actual_result: {actual_result} ==============")
    expected_result = "1"
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"

def test_ios_calculmath_sub_neg_result(driver_setup, appium_capabilities):
    # This check happens at runtime, after appium_capabilities has been resolved
    if appium_capabilities["platform"] != "iOS":
        pytest.skip("Skipping iOS test as current capabilities are not for iOS.")
    
    driver = driver_setup # The driver is provided by the fixture
    
    print("Performing calculation: 2 - 3 = -1 on CalculMath (iOS)")
    
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '2').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '-').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '3').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '=').click()
    
    # time.sleep(1) # Keep the app open for a bit for observation
    
    result_element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'displayValue')
    actual_result = result_element.text
    # print(f"================ iOS add neg res. actual_result: {actual_result} ==============")

    expected_result = "-1" 
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"


