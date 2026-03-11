from pages.inventory_page import InventoryPage
from core.flow_result import FlowResult


class InventoryFlow:

    def __init__(self, driver, settings):

        self.page = InventoryPage(driver, settings)

    def get_inventory_count(self):

        count = self.page.get_product_count()

        return FlowResult(
            success=True,
            data={"count": count},
            message="Inventory loaded"
        )