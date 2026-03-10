import pytest
from appium.webdriver.common.appiumby import AppiumBy

pytestmark = pytest.mark.ios

def test_add(driver):
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "3").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "+").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "2").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "=").click()

    actual = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "displayValue").text
    assert actual == "5"


def test_subtraction_inp_pos_out_pos(driver):
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "3").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "-").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "2").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "=").click()

    actual = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "displayValue").text
    assert actual == "1"


def test_multiplication_fail(driver):
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "3").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "*").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "0").click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "=").click()

    actual = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "displayValue").text
    assert actual == "3"    

