import pytest
import allure

from flows.login_flow import LoginFlow
from flows.logout_flow import LogoutFlow


@allure.tag("logout")

@pytest.mark.logout
def test_logout(driver, test_data, settings):

    login = LoginFlow(driver, settings)

    with allure.step("Login"):
        login.login(
            test_data["username"],
            test_data["password"]
        )

    logout = LogoutFlow(driver, settings)

    with allure.step("Logout"):
        logout.logout()