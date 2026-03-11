import pytest
import allure
from core.driver_manager import DriverManager
import os
import shutil
from datetime import datetime
from utils.error_handler import handle_exception
from config.settings import Settings
import json
import time
from core.data_loader import DataLoader
from utils.screenshot_manager import ScreenshotManager
from collections import defaultdict
from core.execution_tracker import retry_tracker, flaky_tests, current_test

execution_data = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "start_time": 0,
    "end_time": 0,
}

case_execution_data = []

def pytest_sessionstart(session):
    execution_data["start_time"] = time.time()

def pytest_runtest_setup(item):
    module = item.module.__name__
    case = item.name
    current_test = f"{module}::{case}"

def pytest_sessionfinish(session, exitstatus):

    # 计算执行时间
    execution_data["end_time"] = time.time()

    duration = execution_data["end_time"] - execution_data["start_time"]

    env = session.config.getoption("--env")
    browser = session.config.getoption("--browser")

    settings = Settings(env)
    browser = browser or settings.default_browser
    threshold = settings.get_success_threshold

    avg_duration = 0
    slowest_cases = []
    module_success_rate = {}
    top_failed_cases = []

    if case_execution_data:
        # 平均执行时间
        avg_duration = sum(
            case["duration"] for case in case_execution_data
        ) / len(case_execution_data)
        # 最慢用例 只取最慢用例
        slowest_cases = [
            {
                "module": case["module"],
                "case": case["case"],
                "duration": round(case["duration"], 2)
            }
            for case in sorted(
                case_execution_data,
                key=lambda x: x["duration"],
                reverse=True
            )[:5]
        ]
        # 模块成功率
        module_stats = defaultdict(lambda: {"total": 0, "passed": 0})

        for case in case_execution_data:
            module = case["module"]

            module_stats[module]["total"] += 1

            if case["status"] == "passed":
                module_stats[module]["passed"] += 1

        module_success_rate = {}

        for module, stats in module_stats.items():
            rate = round(
                stats["passed"] / stats["total"] * 100,
                2
            )

            module_success_rate[module] = f"{rate}%"

        # 统计失败次数最多的测试用例（Top 5 Failed Cases）
        fail_counter = defaultdict(int)

        for case in case_execution_data:

            if case["status"] == "failed":
                key = f"{case['module']}::{case['case']}"
                fail_counter[key] += 1

        top_failed_cases = [
            {"case": case, "count": count}
            for case, count in sorted(
                fail_counter.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]


    # 统计成功率
    summary = {
        "env": env,
        "browser": browser,
        "total": execution_data["total"],
        "passed": execution_data["passed"],
        "failed": execution_data["failed"],
        "skipped": execution_data["skipped"],
        "total_duration": round(duration, 2),
        "success_rate": round(
            execution_data["passed"] / execution_data["total"] * 100, 2
        ) if execution_data["total"] > 0 else 0,

        "average_duration": round(avg_duration, 2),

        "slowest_cases": slowest_cases,

        "module_success_rate": module_success_rate,

        "top_failed_cases": top_failed_cases
    }

    os.makedirs("reports", exist_ok=True)

    #写execution_summary.json
    with open("reports/execution_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # Flaky Test
    for case, retry_count in retry_tracker.items():
        # 找最终结果
        final_status = None

        for c in case_execution_data:
            if c["case"] == case:
                final_status = c["status"]
                break

        # 只有 retry 且最终成功 才算 flaky
        if retry_count > 0 and final_status == "passed":
            flaky_tests.append({
                "case": case,
                "retry": retry_count
            })
    flaky_report = {
        "flaky_tests": flaky_tests
    }

    with open("reports/flaky_tests.json", "w", encoding="utf-8") as f:
        json.dump(flaky_report, f, indent=4)

    total_tests = execution_data["total"]
    flaky_count = len(flaky_tests)

    flaky_rate = 0

    if total_tests > 0:
        flaky_rate = round(flaky_count / total_tests * 100, 2)

    flaky_report = {
        "total_tests": total_tests,
        "flaky_tests": flaky_count,
        "flaky_rate": flaky_rate,
        "unstable_tests": flaky_tests
    }

    with open("reports/flaky_report.json", "w", encoding="utf-8") as f:
        json.dump(flaky_report, f, indent=4)

    #判断 CI 是否失败
    if summary["success_rate"] < threshold:
        print(f"\n⚠ Success rate below {threshold}%! Failing build.")
        # 0 = 全部通过  1 = 有失败
        session.exitstatus = 1
    print(f"\nFinal exit status: {session.exitstatus}")

    # copy categories.json to allure-results
    categories_src = os.path.join("reports", "categories.json")
    categories_dst = os.path.join("reports", "allure-results", "categories.json")

    if os.path.exists(categories_src):
        shutil.copy(categories_src, categories_dst)

@pytest.fixture(scope="function")
def driver(request, settings):
    # 读取命令行参数
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    # 如果命令行没传 browser，就用 config 里的默认
    browser = browser or settings.default_browser
    print(f"Running ENV: {settings.env}")
    print(f"Running Browser: {browser}")

    driver = DriverManager.create_driver(browser=browser, headless=headless)
    # driver.get(settings.base_url)
    yield driver
    DriverManager.quit_driver(driver)

# def pytest_generate_tests(metafunc):
#     # metafunc.fixturenames 是： 当前 test 函数声明的参数列表
#     if "test_data" not in metafunc.fixturenames:
#         return
#
#     # 1️⃣ 读取 test 上的 module 标记  @pytest.mark.module("login")
#     marker = metafunc.definition.get_closest_marker("module")
#     if not marker:
#         return
#
#     test_module = marker.args[0]
#
#     # 2️⃣ 读取命令行 module
#     cmd_module = metafunc.config.getoption("--module")
#
#     # 如果命令行指定了 module，但和当前 test 不一致 → 不参数化
#     if cmd_module and test_module != cmd_module:
#         return
#
#     # 3️⃣ 读取环境
#     env = metafunc.config.getoption("--env")
#     settings = Settings(env)
#
#     # 4️⃣ 拼路径
#     file_path = os.path.join(
#         settings.get_data_dir,
#         test_module,
#         f"{test_module}_data.yaml"
#     )
#
#     # 5️⃣ 加载数据
#     data = DataLoader.load_yaml(
#         file_path,
#         f"{test_module}_cases"
#     )
#     # 相当于@pytest.mark.parametrize 参数化
#     metafunc.parametrize("test_data", data)

def pytest_generate_tests(metafunc):
    # metafunc.fixturenames 是： 当前 test 函数声明的参数列表
    if "test_data" not in metafunc.fixturenames:
        return

    # module_name = None
    # # 遍历当前测试函数上的所有 marker  例如：@pytest.mark.login  login 就是一个 marker
    # for mark in metafunc.definition.iter_markers():
    #     # 取第一个 marker 的名字，赋值给 module_name，然后立刻退出循环，因为只需要第一个 marker
    #     # 取测试函数的第一个 marker 名字，例如一个函数上有2个marker
    #     # @pytest.mark.login
    #     # @pytest.mark.smoke
    #     # 它只会取：login
    #     module_name = mark.name
    #     break
    #
    # if not module_name:
    #     # 如果没有获取到 marker，直接结束函数
    #     return
    # # 1️⃣ 读取 test 上的 module 标记  @pytest.mark.module("login")
    # marker = metafunc.definition.get_closest_marker("module")
    # if not marker:
    #     return
    #
    # test_module = marker.args[0]

    # # 2️⃣ 读取命令行 module
    # cmd_module = metafunc.config.getoption("--module")
    #
    # # 如果命令行指定了 module，但和当前 test 不一致 → 不参数化
    # if cmd_module and module_name != cmd_module:
    #     return

    # 3️⃣ 读取环境
    env = metafunc.config.getoption("--env")
    settings = Settings(env)

    data_root = settings.get_data_dir
    # 自动扫描 data 目录
    available_modules = []
    # 获取 data_root 目录下所有“子目录”的名字，结果是一个 list
    for name in os.listdir(data_root):
        path = os.path.join(data_root, name)

        if os.path.isdir(path):
            available_modules.append(name)

    module_name = None
    # 遍历当前测试函数上的所有 marker  例如：@pytest.mark.login  login 就是一个 marker
    for mark in metafunc.definition.iter_markers():
        if mark.name in available_modules:
            module_name = mark.name
            break

    if not module_name:
        return

    # 4️⃣ 拼路径
    file_path = os.path.join(
        settings.get_data_dir,
        module_name,
        f"{module_name}_data.yaml"
    )

    # 5️⃣ 加载数据
    data = DataLoader.load_yaml(
        file_path,
        f"{module_name}_cases"
    )
    # 相当于@pytest.mark.parametrize 参数化
    metafunc.parametrize("test_data", data)


@pytest.fixture(scope="session")
def settings(request):
    env = request.config.getoption("--env")
    return Settings(env)

# 我正在实现（implement）一个 pytest 的 hook（钩子函数），我要“包裹”这个 hook，先执行我的代码，再执行原本 pytest 的代码，执行完再回到我这里
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 让pytest先执行测试
    outcome = yield
    # 拿到结果
    report = outcome.get_result()

    # ===== 执行统计逻辑（保持不变） =====
    if report.when == "call":

        module_name = item.module.__name__
        case_name = item.name

        case_execution_data.append({
            "module": module_name,
            "case": case_name,
            "duration": report.duration,
            "status": report.outcome
        })

        execution_data["total"] += 1

        if report.passed:
            execution_data["passed"] += 1
        elif report.failed:
            execution_data["failed"] += 1
        elif report.skipped:
            execution_data["skipped"] += 1

    # ===== 失败处理 =====
    if report.when == "call" and report.failed:
        handle_exception(call)
        # item 是当前正在执行的测试用例对象，它包含用例名称，所在文件，fixture 参数，测试函数本身，运行状态等等
        # funcargs 是一个字典，它保存了当前测试函数注入的所有 fixture 参数：从 funcargs 里取 driver，如果没有，就返回 None
        # 如果当前 test case 使用了 driver 这个 fixture，那我就把它拿出来
        driver = item.funcargs.get("driver", None)
        if driver:
            # 当前测试用例所在的 Python 文件名，例如文件是test_login.py，那module_name = "test_login"
            module_name = item.module.__name__
            # 当前测试函数名，例如：def test_login_success():，那么case_name = "test_login_success"
            case_name = item.name

            ScreenshotManager.capture(
                driver,
                module_name,
                case_name
            )
            # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # filename = f"{item.name}_{timestamp}.png"
            # screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            #
            # os.makedirs(screenshots_dir, exist_ok=True)
            #
            # file_path = os.path.join(screenshots_dir, filename)
            # driver.save_screenshot(file_path)
            #
            # # 🔥 attach to allure
            # with open(file_path, "rb") as f:
            #     allure.attach(
            #         f.read(),
            #         name="Failure Screenshot",
            #         attachment_type=allure.attachment_type.PNG
            #     )

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment"
    )

    parser.addoption(
        "--browser",
        action="store",
        help="Browser type"
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="rRun headless"
    )

    parser.addoption("--module", action="store", default="login")