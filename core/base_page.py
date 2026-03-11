from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

from core.retry import retry
from utils.logger import get_logger


class BasePage:

    def __init__(self, driver, settings):

        self.driver = driver
        self.settings = settings
        self.logger = get_logger()

        self.wait = WebDriverWait(driver, settings.timeout)

    # =================================
    # Element Find
    # =================================

    def find(self, locator):
        """
        Find single element
        """
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator):
        """
        Find multiple elements
        """
        return self.driver.find_elements(*locator)

    # =================================
    # Click Operations
    # =================================

    @retry(times=2, delay=1)
    def click(self, locator):
        """
        Normal click
        """
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.logger.info(f"Click element: {locator}")

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element
        )

        element.click()

        return element

    @retry(times=2, delay=1)
    def safe_click(self, locator):
        """
        Scroll + Click
        Prevent click intercepted
        """

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.scroll_to_element(locator)

        self.logger.info(f"Safe click: {locator}")

        element.click()

        return element

    def js_click(self, locator):
        """
        Click using JavaScript
        """
        element = self.find(locator)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        self.logger.info(f"JS click: {locator}")

    # =================================
    # Input
    # =================================

    @retry(times=2, delay=1)
    def input(self, locator, text):

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            element.clear()
            element.send_keys(text)

            self.logger.info(f"Input text into {locator}")

        except TimeoutException:

            raise TimeoutException("[TIMEOUT_ERROR] Wait timeout")

    # =================================
    # State Check
    # =================================

    def is_element_visible(self, locator):

        try:

            self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            return True

        except TimeoutException:

            return False

    # =================================
    # Wait Utilities
    # =================================

    def wait_for_visible(self, locator):

        self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator):

        self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_text(self, locator, text):

        self.wait.until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def wait_for_element_count(self, locator, count):

        self.wait.until(
            lambda d: len(d.find_elements(*locator)) == count
        )

    def wait_url_contains(self, text):

        self.wait.until(
            EC.url_contains(text)
        )

    def wait_for_page_ready(self):
        """
        Wait until page fully loaded
        """

        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    # =================================
    # Scroll
    # =================================

    def scroll_to_element(self, locator):

        element = self.find(locator)

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )

        return element

    # =================================
    # Mouse Actions
    # =================================

    def hover(self, locator):

        element = self.find(locator)

        ActionChains(self.driver).move_to_element(
            element
        ).perform()

        self.logger.info(f"Hover on element: {locator}")

    def drag_and_drop(self, source_locator, target_locator):

        source = self.find(source_locator)
        target = self.find(target_locator)

        ActionChains(self.driver).drag_and_drop(
            source,
            target
        ).perform()

        self.logger.info(
            f"Drag {source_locator} to {target_locator}"
        )