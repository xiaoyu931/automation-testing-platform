from selenium.webdriver.common.by import By
from core.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (By.ID, "user-name")

    PASSWORD = (By.ID, "password")

    LOGIN_BTN = (By.ID, "login-button")

    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")

    INVENTORY_TITLE = (By.CLASS_NAME, "title")

    def login(self, username, password):

        self.input(self.USERNAME, username)

        self.input(self.PASSWORD, password)

        self.safe_click(self.LOGIN_BTN)

    def is_login_failed(self):

        return self.is_element_visible(self.ERROR_MSG)

    def is_inventory_page_displayed(self):

        return self.is_element_visible(self.INVENTORY_TITLE)