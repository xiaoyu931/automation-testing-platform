import pytest
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@allure.tag("failure")
@allure.epic("CRM Automation System")
@allure.feature("Failure Demo")
@allure.story("Timeout Failure")

@pytest.mark.failure
def test_timeout_failure(driver):
    """
    Intentionally trigger TimeoutException
    """

    driver.get("https://www.saucedemo.com")

    with allure.step("Wait for non-existing element"):

        WebDriverWait(driver, 2).until(
            lambda d: d.find_element(By.ID, "not_exist_element")
        )