import random
import pytest
import allure
from core.retry import retry

@allure.feature("Flaky Tests")
@allure.story("Random failure")
@pytest.mark.flaky
@retry(times=2, delay=1)
def test_random_flaky():

    result = random.choice([True, False])

    if not result:
        raise Exception("Random flaky failure")