import pytest
from core.execution_tracker import current_test


def pytest_runtest_setup(item):

    module = item.module.__name__
    case = item.name

    current_test.value = f"{module}::{case}"