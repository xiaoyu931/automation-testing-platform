from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from core.flow_result import FlowResult


class AddToCartFlow:

    def __init__(self, driver, settings):

        self.inventory = InventoryPage(driver, settings)

        self.cart = CartPage(driver, settings)

    def add_product(self):

        self.inventory.wait_for_page_ready()

        self.inventory.add_backpack_to_cart()

        count = self.inventory.get_cart_badge_count()

        return FlowResult(
            success=True,
            data={"cart_count": count},
            message="Product added to cart"
        )