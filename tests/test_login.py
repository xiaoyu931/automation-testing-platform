import pytest
import allure

from flows.login_flow import LoginFlow
from assertions.assert_utils import AssertUtils


@allure.tag("login")
@allure.epic("CRM Automation System")
@allure.feature("User Authentication")
@allure.story("Multi-account Login Validation")
@allure.severity(allure.severity_level.CRITICAL)

@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
def test_login(driver, test_data, settings):

    flow = LoginFlow(driver, settings)

    with allure.step(f"Execute login flow | user={test_data['username']}"):

        result = flow.login(
            test_data["username"],
            test_data["password"]
        )

    with allure.step("Validate login result"):

        AssertUtils.assert_equal(
            result.success,
            test_data["expected"],
            "Login result validation"
        )