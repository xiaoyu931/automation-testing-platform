import random
import time
import pytest
import allure
from core.retry import retry

@allure.feature("Flaky Tests")
@allure.story("Slow response")
@pytest.mark.flaky
@retry(times=2, delay=1)
def test_slow_response():

    delay = random.uniform(0, 3)

    time.sleep(delay)

    if delay > 1:
        raise Exception("Service response too slow")