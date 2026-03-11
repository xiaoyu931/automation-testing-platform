from config.settings import Settings
import pytest


@pytest.fixture(scope="session")
def settings(request):
    env = request.config.getoption("--env")
    return Settings(env)