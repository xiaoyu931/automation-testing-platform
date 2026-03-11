import pytest
from utils.error_handler import handle_exception
from utils.screenshot_manager import ScreenshotManager
from hooks.execution_hook import execution_data, case_execution_data


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # 我正在实现（implement）一个 pytest 的 hook（钩子函数）
    # 我要“包裹”这个 hook
    # 先执行我的代码
    # 再执行原本 pytest 的代码
    # 执行完再回到我这里

    outcome = yield

    report = outcome.get_result()

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

        driver = item.funcargs.get("driver", None)

        if driver:

            module_name = item.module.__name__
            case_name = item.name

            ScreenshotManager.capture(
                driver,
                module_name,
                case_name
            )