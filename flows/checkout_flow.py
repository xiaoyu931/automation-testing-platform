from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from core.flow_result import FlowResult


class CheckoutFlow:

    def __init__(self, driver, settings):

        self.cart = CartPage(driver, settings)
        self.checkout = CheckoutPage(driver, settings)

    def complete_checkout(self, first, last, zip):

        self.cart.checkout()

        self.checkout.fill_checkout_info(first, last, zip)

        # 如果输入错误
        if self.checkout.is_checkout_failed():

            return FlowResult(
                success=False,
                data={"message": self.checkout.get_error_message()},
                message="Checkout failed"
            )

        # 正常 checkout
        self.checkout.finish_checkout()

        message = self.checkout.get_success_message()

        return FlowResult(
            success=True,
            data={"message": message},
            message="Checkout finished"
        )