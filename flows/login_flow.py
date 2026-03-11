from pages.login_page import LoginPage
from core.flow_result import FlowResult


class LoginFlow:

    def __init__(self, driver, settings):

        self.driver = driver
        self.settings = settings

        self.page = LoginPage(driver, settings)

    def login(self, username, password):

        self.driver.get(self.settings.base_url)

        self.page.wait_for_page_ready()

        self.page.login(username, password)

        # 登录成功
        if self.page.is_inventory_page_displayed():

            return FlowResult(
                success=True,
                data={"username": username},
                message="Login success"
            )

        # 登录失败
        if self.page.is_login_failed():

            return FlowResult(
                success=False,
                data={"username": username},
                message="Login failed"
            )

        return FlowResult(
            success=False,
            message="Unknown login result"
        )