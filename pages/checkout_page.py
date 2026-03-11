from selenium.webdriver.common.by import By
from core.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")

    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")

    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")

    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")

    def fill_checkout_info(self, first, last, zip):

        self.input(self.FIRST_NAME, first)
        self.input(self.LAST_NAME, last)
        self.input(self.ZIP, zip)

        self.click(self.CONTINUE)

    def is_checkout_failed(self):

        return self.is_element_visible(self.ERROR_MSG)

    def get_error_message(self):

        return self.find(self.ERROR_MSG).text

    def finish_checkout(self):

        self.wait_for_clickable(self.FINISH)
        self.click(self.FINISH)

    def get_success_message(self):

        return self.find(self.SUCCESS_MSG).text