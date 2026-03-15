import time
import functools
from utils.logger import get_logger

logger = get_logger()


def retry(times=2, delay=1, exceptions=(Exception,)):
    """
    通用重试装饰器
    :param times: 最大尝试次数
    :param delay: 重试间隔
    :param exceptions: 捕获异常
    """
    # 这里：func 就是被装饰的函数，例如：
    # @retry()
    # def test_login():
    # 这里：func = test_login
    def decorator(func):

        @functools.wraps(func) # 保留原函数的名字、注释等信息。否则装饰后函数名会变成： wrapper，而不是原函数名。
        def wrapper(*args, **kwargs):
        # 这是 真正执行函数的地方，*args, **kwargs 表示：支持任何参数。例如；login(user, password)
            # 记录最后一次异常，如果所有重试都失败，抛出最后一次异常
            last_exception = None
            # 重试循环
            for attempt in range(1, times + 1):

                try:
                    # 尝试执行函数，如果执行成功，直接返回结果，结束重试
                    # 这一行代码等价于：
                    # result = func(*args, **kwargs)
                    # return result
                    # 如果 func() 抛异常：就会进入：except
                    # 如果成功的话，就直接返回了
                    return func(*args, **kwargs)

                except exceptions as e:

                    if isinstance(e, AssertionError):
                        # 断言失败不要重试
                        raise
                    # 保存最后一次错误。
                    last_exception = e
                    # 打印 warning 日志，例如：[Retry] test_login failed (attempt 1/3) -> TimeoutError
                    logger.warning(
                        f"[Retry] {func.__name__} failed "
                        f"(attempt {attempt}/{times}) -> {e}"
                    )
                    # 等待后重试
                    if attempt < times:
                        time.sleep(delay)
            # 所有重试失败，输出：[Retry] test_login failed after 3 attempts
            logger.error(
                f"[Retry] {func.__name__} failed after {times} attempts"
            )
            # 抛出最后异常，这样测试框架就能识别失败。
            raise last_exception
        # 返回包装后的函数
        return wrapper
    # 最终形成装饰器
    return decorator