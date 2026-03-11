from utils.logger import get_logger
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)

logger = get_logger("error_handler")

def handle_exception(call):

    if not call.excinfo:
        return
    logger.error(
        "Test Failed"
    )
    exc_type = call.excinfo.type
    exc_value = call.excinfo.value
    msg = str(exc_value).split("\n")[0]

    logger.error(f"Exception Type: {exc_type.__name__}")
    logger.error(f"Exception Message: {msg}")


    # 分类处理
    if issubclass(exc_type, AssertionError):
        logger.error("[ASSERTION_ERROR] Business logic failed")

    elif issubclass(exc_type, NoSuchElementException):
        logger.error("[LOCATOR_ERROR] Element not found")

    elif issubclass(exc_type, TimeoutException):
        logger.error("[TIMEOUT_ERROR] Wait timeout")

    elif issubclass(exc_type, ElementClickInterceptedException):
        logger.error("[CLICK_ERROR] Click intercepted")

    elif issubclass(exc_type, StaleElementReferenceException):
        logger.warning("[STALE_ELEMENT] DOM refreshed")

    elif issubclass(exc_type, WebDriverException):
        logger.error("[NETWORK_OR_BROWSER_ERROR] WebDriver issue")

    else:
        logger.error("[UNKNOWN_ERROR] Unhandled exception")

