import pytest
from appium.webdriver.common.appiumby import AppiumBy

pytestmark = pytest.mark.android

# @pytest.mark.android
def test_add(driver):
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_3").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/op_add").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_2").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/eq").click()

    result_element = driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_final")
    actual = result_element.text

    assert actual == "5"

# @pytest.mark.android
def test_subtraction_inp_pos_out_pos(driver):
    # driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/op_sub").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_3").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/op_sub").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_2").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/eq").click()

    result_element = driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_final")
    # actual = driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_final")
    actual = result_element.text
    # print(f"================ actual:{actual} ====================")

    # assert actual.replace('-', '−') == '−1'
    # assert actual == '−1'
    # assert actual == '-1'
    assert actual == '1'







