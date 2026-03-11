import pytest
import allure

from selenium.webdriver.common.by import By


@allure.tag("failure")
@allure.epic("CRM Automation System")
@allure.feature("Failure Demo")
@allure.story("Element Not Found")

@pytest.mark.failure
def test_element_failure(driver):
    """
    Intentionally trigger NoSuchElementException
    """

    driver.get("https://www.saucedemo.com")

    with allure.step("Find non-existing element"):

        driver.find_element(By.ID, "element_not_exist")