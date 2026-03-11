from utils.logger import get_logger

logger = get_logger()

class AssertUtils:

    @staticmethod
    def assert_true(condition, message="Assertion failed"):
        if not condition:
            logger.error(f"[ASSERT FAIL] {message}")
            raise AssertionError(message)
        logger.info(f"[ASSERT PASS] {message}")

    @staticmethod
    def assert_false(condition, message="Assertion failed"):
        if condition:
            logger.error(f"[ASSERT FAIL] {message}")
            raise AssertionError(message)
        logger.info(f"[ASSERT PASS] {message}")

    @staticmethod
    def assert_equal(actual, expected, message="Values not equal"):
        if actual != expected:
            full_message = f"{message} | actual = {actual}, expected = {expected}"
            logger.error(f"[ASSERT FAIL] { full_message}")
            raise AssertionError(full_message)
        logger.info(f"[ASSERT PASS] {message}")


    @staticmethod
    def assert_url_contains(driver, text, message=None):
        if text not in driver.current_url:
            msg = message or f"URL does not contain '{text}'"
            logger.error(f"[ASSERT FAIL] {msg}")
            raise AssertionError(msg)
        logger.info(f"[ASSERT PASS] URL contains '{text}'")