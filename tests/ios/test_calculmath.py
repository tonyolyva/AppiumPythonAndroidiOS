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