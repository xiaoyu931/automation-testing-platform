import time
import functools
from utils.logger import get_logger
from core.execution_tracker import retry_tracker, current_test

logger = get_logger()

# 接收参数
def retry(times=2, delay=1, exceptions=(Exception,)):
    """
    通用重试装饰器
    :param times: 重试次数
    :param delay: 每次重试间隔秒数
    :param exceptions: 捕获哪些异常,哪些异常才进行重试
    """
    # 接收被装饰的函数。# 接收函数
    def decorator(func):
        # 让被装饰后的函数，保留原函数的名字、文档、注释等信息。 否则函数会“变成” wrapper
        @functools.wraps(func)
        # 真正执行函数的地方。 *args → 位置参数  **kwargs → 关键字参数  保证兼容所有函数  # 执行函数
        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(1, times + 1):
                try:
                    # 记录当前重试次数
                    wrapper.current_attempt = attempt
                    # 尝试执行函数 直接返回结果  不再重试
                    return func(*args, **kwargs)
                #只捕获指定异常类型。
                except exceptions as e:

                    # ❗ 不重试 AssertionError
                    if isinstance(e, AssertionError):
                        raise

                    last_exception = e
                    retry_tracker[current_test.value] += 1

                    logger.warning(
                        f"[Retry] {func.__name__} failed "
                        f"(attempt {attempt}/{times}) "
                        f"-> {e}"
                    )
                    try:
                        self_obj = args[0]
                        driver = getattr(self_obj, "driver", None)

                        if driver:
                            from utils.screenshot_manager import ScreenshotManager
                            ScreenshotManager.capture(
                                driver,
                                module_name=func.__module__,
                                case_name=str(current_test),
                                retry_index=attempt
                            )
                    except Exception:
                        pass

                    if attempt < times:
                        time.sleep(delay)

            logger.error(
                f"[Retry] {current_test.value} failed after {times} attempts"
            )

            raise last_exception

        # 把原函数 func 替换成 wrapper  本质上，原函数被 wrapper 接管了。
        return wrapper
    # 把真正的装饰器函数交出去
    return decorator
