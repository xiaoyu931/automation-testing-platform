from selenium.webdriver.common.by import By
from core.base_page import BasePage


class InventoryPage(BasePage):

    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")

    def add_backpack_to_cart(self):

        self.click(self.ADD_BACKPACK)

    def get_cart_badge_count(self):

        if self.is_element_visible(self.CART_BADGE):

            return int(self.find(self.CART_BADGE).text)

        return 0

    def get_inventory_items(self):

        return self.find_all(self.INVENTORY_ITEMS)

    def get_product_count(self):
        items = self.find_all(self.INVENTORY_ITEMS)

        return len(items)