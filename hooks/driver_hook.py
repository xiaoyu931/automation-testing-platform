import pytest
from core.driver_manager import DriverManager


@pytest.fixture(scope="function")
def driver(request, settings):

    # 读取命令行参数
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    # 如果命令行没传 browser，就用 config 里的默认
    browser = browser or settings.default_browser

    print(f"Running ENV: {settings.env}")
    print(f"Running Browser: {browser}")

    driver = DriverManager.create_driver(
        browser=browser,
        headless=headless
    )

    yield driver

    DriverManager.quit_driver(driver)