import pytest
import allure

from flows.login_flow import LoginFlow


@allure.tag("failure")
@allure.epic("CRM Automation System")
@allure.feature("Failure Demo")
@allure.story("Assertion Failure")

@pytest.mark.failure
def test_assertion_failure(driver, settings):
    """
    Intentionally trigger AssertionError
    Used for testing:
    - error classification
    - screenshot
    - allure categories
    """

    flow = LoginFlow(driver, settings)

    with allure.step("Execute login flow"):

        result = flow.login(
            "standard_user",
            "secret_sauce"
        )

    with allure.step("Force assertion failure"):

        assert False, "Intentional assertion failure"