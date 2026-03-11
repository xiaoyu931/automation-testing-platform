import pytest
import allure

from flows.login_flow import LoginFlow


@allure.tag("failed")
@allure.epic("CRM Automation System")
@allure.feature("Failure Demo")
@allure.story("Intentional Failure Test")
@allure.severity(allure.severity_level.CRITICAL)

@pytest.mark.failed
def test_fail(driver, settings):
    """
    Demo test used to trigger failure
    Used for:
    - error classification
    - screenshot capture
    - retry validation
    """

    flow = LoginFlow(driver, settings)

    with allure.step("Execute login flow with valid credentials"):

        result = flow.login(
            "standard_user",
            "secret_sauce"
        )

    with allure.step("Force failure to test framework error handling"):

        assert False