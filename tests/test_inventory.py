import pytest
import allure

from flows.login_flow import LoginFlow
from flows.inventory_flow import InventoryFlow
from assertions.assert_utils import AssertUtils


@allure.tag("inventory")
@allure.feature("Inventory")

@pytest.mark.inventory
def test_inventory(driver, test_data, settings):

    login = LoginFlow(driver, settings)

    with allure.step("Login"):
        login.login(
            test_data["username"],
            test_data["password"]
        )

    inventory = InventoryFlow(driver, settings)

    with allure.step("Load inventory"):
        result = inventory.get_inventory_count()

    with allure.step("Validate product count"):

        AssertUtils.assert_equal(
            result.data["count"],
            test_data["expected_count"],
            "Inventory count validation"
        )