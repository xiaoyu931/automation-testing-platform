from pages.menu_page import MenuPage
from core.flow_result import FlowResult


class LogoutFlow:

    def __init__(self, driver, settings):

        self.page = MenuPage(driver, settings)

    def logout(self):

        self.page.open_menu()

        self.page.logout()

        return FlowResult(
            success=True,
            message="Logout success"
        )