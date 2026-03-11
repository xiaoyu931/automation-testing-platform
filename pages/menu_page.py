from selenium.webdriver.common.by import By
from core.base_page import BasePage


class MenuPage(BasePage):

    MENU_BTN = (By.ID, "react-burger-menu-btn")

    LOGOUT_BTN = (By.ID, "logout_sidebar_link")

    def open_menu(self):

        self.safe_click(self.MENU_BTN)

    def logout(self):

        self.wait_for_visible(self.LOGOUT_BTN)
        self.safe_click(self.LOGOUT_BTN)