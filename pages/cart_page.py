from selenium.webdriver.common.by import By
from core.base_page import BasePage


class CartPage(BasePage):

    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    CHECKOUT_BTN = (By.ID, "checkout")

    CART_ITEMS = (By.CLASS_NAME, "cart_item")

    def open_cart(self):

        self.click(self.CART_ICON)

    def checkout(self):

        self.open_cart()

        self.wait_for_clickable(self.CHECKOUT_BTN)

        self.click(self.CHECKOUT_BTN)

    def get_cart_items(self):

        return self.find_all(self.CART_ITEMS)

    def get_cart_count(self):

        items = self.get_cart_items()

        return len(items)