import pytest
import allure

from flows.login_flow import LoginFlow
from flows.add_to_cart_flow import AddToCartFlow
from assertions.assert_utils import AssertUtils


@allure.tag("cart")
@allure.epic("CRM Automation System")
@allure.feature("Shopping Cart")
@allure.story("Add Product To Cart")

@pytest.mark.cart
@pytest.mark.regression
def test_add_to_cart(driver, test_data, settings):

    login = LoginFlow(driver, settings)

    with allure.step("Login"):

        login.login(
            test_data["username"],
            test_data["password"]
        )

    cart = AddToCartFlow(driver, settings)

    with allure.step("Add product to cart"):

        result = cart.add_product()

    with allure.step("Validate cart count"):

        AssertUtils.assert_equal(
            result.data["cart_count"],
            test_data["expected_cart_count"],
            "Cart count validation"
        )