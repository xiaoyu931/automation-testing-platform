import pytest
import os
from config.settings import Settings
from core.data_loader import DataLoader


def pytest_generate_tests(metafunc):

    # metafunc.fixturenames 是： 当前 test 函数声明的参数列表
    if "test_data" not in metafunc.fixturenames:
        return

    env = metafunc.config.getoption("--env")

    settings = Settings(env)

    data_root = settings.get_data_dir

    # 自动扫描 data 目录
    available_modules = []

    for name in os.listdir(data_root):

        path = os.path.join(data_root, name)

        if os.path.isdir(path):

            available_modules.append(name)

    module_name = None

    # 遍历当前测试函数上的所有 marker
    for mark in metafunc.definition.iter_markers():

        if mark.name in available_modules:

            module_name = mark.name

            break

    if not module_name:
        return

    file_path = os.path.join(
        settings.get_data_dir,
        module_name,
        f"{module_name}_data.yaml"
    )

    data = DataLoader.load_yaml(
        file_path,
        f"{module_name}_cases"
    )

    metafunc.parametrize("test_data", data)