import pytest
from appium.webdriver.common.appiumby import AppiumBy

pytestmark = pytest.mark.android

@pytest.mark.android
def test_add(driver):
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_3").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/op_add").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/digit_2").click()
    driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/eq").click()

    actual = driver.find_element(AppiumBy.ID, "com.google.android.calculator:id/result_final").text
    assert actual == "5"


