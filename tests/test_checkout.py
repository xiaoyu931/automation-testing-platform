import pytest
import allure

from flows.login_flow import LoginFlow
from flows.add_to_cart_flow import AddToCartFlow
from flows.checkout_flow import CheckoutFlow
from assertions.assert_utils import AssertUtils


@allure.tag("checkout")
@allure.epic("CRM Automation System")
@allure.feature("Checkout")
@allure.story("Complete Order")

@pytest.mark.checkout
@pytest.mark.regression
def test_checkout(driver, test_data, settings):

    login = LoginFlow(driver, settings)

    with allure.step("Login"):

        login.login(
            test_data["username"],
            test_data["password"]
        )

    cart_flow = AddToCartFlow(driver, settings)

    with allure.step("Add product to cart"):

        cart_flow.add_product()

    checkout = CheckoutFlow(driver, settings)

    with allure.step("Checkout"):

        result = checkout.complete_checkout(
            test_data["first_name"],
            test_data["last_name"],
            test_data["zip"]
        )

    with allure.step("Validate checkout result"):

        AssertUtils.assert_equal(
            result.data["message"],
            test_data["expected_message"],
            "Checkout validation"
        )