import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.web

BASE_URL = "http://127.0.0.1:8000/webapp/"


def test_page_loads(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("CalculMath Web")
    expect(page.get_by_test_id("display")).to_have_value("0")


def test_addition(page: Page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="3").click()
    page.get_by_role("button", name="+").click()
    page.get_by_role("button", name="2").click()
    page.get_by_role("button", name="=").click()
    expect(page.get_by_test_id("display")).to_have_value("5")


def test_clear(page: Page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="9").click()
    page.get_by_role("button", name="C").click()
    expect(page.get_by_test_id("display")).to_have_value("0")