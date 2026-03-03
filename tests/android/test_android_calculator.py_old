import pytest
from appium.webdriver.common.appiumby import AppiumBy
import time

def test_android_calculator_add_pos_result(driver_setup, appium_capabilities):
    # This check happens at runtime, after appium_capabilities has been resolved
    if appium_capabilities["platform"] != "Android":
        pytest.skip("Skipping Android test as current capabilities are not for Android.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 3 + 2 = 5 on Calculator (Android)")
    # driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/clr').click()
    # print("Clicked AC")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_3').click()
    print("Clicked 2")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/op_add').click()
    print("Clicked +")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_2').click()
    print("Clicked 3")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/eq').click()
    print("Clicked =")

    # time.sleep(0.5) # Small pause

    result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/result_final')
    # result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/formula')
    actual_result = result_element.text
    print(f"Actual result: {actual_result}")

    expected_result = "5" 
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"


def test_android_calculator_mul_pos_result(driver_setup, appium_capabilities):
    if appium_capabilities["platform"] != "Android":
        pytest.skip("Skipping Android test as current capabilities are not for Android.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 3 * 2 = 6 on Calculator (Android)")

    # Clear previous entry
    # driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/clr').click()
    # print("Clicked AC")

    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_3').click()
    print("Clicked 3")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/op_mul').click()
    print("Clicked +")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_2').click()
    print("Clicked 2")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/eq').click()
    print("Clicked =")

    # time.sleep(0.5) # Small pause to allow result to display

    # Get the actual result text
    result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/result_final')
    # result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/formula')
    actual_result = result_element.text
    expected_result = "6"

    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result})"
    
def test_android_calculator_sub_pos_result(driver_setup, appium_capabilities):
    if appium_capabilities["platform"] != "Android":
        pytest.skip("Skipping Android test as current capabilities are not for Android.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 3 - 2 = 1 on Calculator (Android)")

    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_3').click()
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/op_sub').click()
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_2').click()
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/eq').click()

    result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/result_final')
    actual_result = result_element.text
    # print(f"================ andr sub pos res. actual_result: {actual_result} ==============")

    expected_result = "1"

    assert actual_result == expected_result, f"Actual {expected_result} but got {actual_result}"

def test_android_calculator_sub_neg_result(driver_setup, appium_capabilities):
    if appium_capabilities["platform"] != "Android":
        pytest.skip("Skipping Android test as current capabilities are not for Android.")

    driver = driver_setup # The driver is provided by the fixture

    print("Performing calculation: 2 - 3 = -1 on Calculator (Android)")

    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_2').click()
    print("Clicked 3")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/op_sub').click()
    print("Clicked +")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/digit_3').click()
    print("Clicked 2")
    driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/eq').click()
    print("Clicked =")

    # time.sleep(0.5) # Small pause to allow result to display

    # Get the actual result text
    result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/result_final')
    # result_element = driver.find_element(AppiumBy.ID, 'com.google.android.calculator:id/formula')
    actual_result = result_element.text

    # Replace the Unicode minus sign with a standard hyphen-minus
    # The calculator app likely returns U+2212 MINUS SIGN (unicode)
    # We want to compare it to U+002D HYPHEN-MINUS (standard keyboard hyphen)
    normalized_actual_result = actual_result.replace('−', '-') # Replace '−' (U+2212) with '-' (U+002D)

    print(f"Actual result (raw): '{actual_result}'")
    print(f"Actual result (normalized): '{normalized_actual_result}'")

    expected_result = "-1"

    assert normalized_actual_result == expected_result, f"Expected {expected_result} but got {normalized_actual_result} (originally: {actual_result})"
    