from pages.login_page import LoginPage
import allure
import pytest
from assertions.assert_utils import AssertUtils

@allure.epic("Baidu System")
@allure.feature("User Authentication")
@allure.story("Single Login Validation")
@allure.severity(allure.severity_level.CRITICAL)
# @pytest.mark.module("change")
@pytest.mark.smoke
@pytest.mark.change
@pytest.mark.failed
def test_login_success(driver, settings):
    with allure.step(f"Login with standard_user"):
        driver.get("https://www.baidu.com/")

        page = LoginPage(driver, settings)
        page.login("standard_user", "secret_sauce")
    with allure.step("Verify login result"):
        # assert "inventory" in driver.current_url
        AssertUtils.assert_url_contains(
            driver,
            "inventory",
            # "inventory wan",
            "Login success URL validation"
        )

