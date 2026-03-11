import pytest
import os
import json
import time
from datetime import datetime
import shutil
from collections import defaultdict
from config.settings import Settings
from core.execution_tracker import retry_tracker, flaky_tests
from utils.analytics_dashboard import generate_dashboard

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

        # 最慢用例
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

        for module, stats in module_stats.items():

            rate = round(
                stats["passed"] / stats["total"] * 100,
                2
            )

            module_success_rate[module] = f"{rate}%"

        # Top 失败用例
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

    with open("reports/execution_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # 写入历史记录
    history_file = "reports/history.json"

    history_data = {"runs": []}

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history_data = json.load(f)

    run_record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": summary["total"],
        "passed": summary["passed"],
        "failed": summary["failed"],
        "success_rate": summary["success_rate"],
        "avg_duration": summary["average_duration"]
    }

    history_data["runs"].append(run_record)

    # 保留最近50次执行
    history_data["runs"] = history_data["runs"][-50:]

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)

    # Flaky Test
    for case, retry_count in retry_tracker.items():

        final_status = None

        for c in case_execution_data:
            if c["case"] == case:
                final_status = c["status"]
                break

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

    # 判断 CI 是否失败
    if summary["success_rate"] < threshold:

        print(f"\n⚠ Success rate below {threshold}%! Failing build.")

        session.exitstatus = 1

    print(f"\nFinal exit status: {session.exitstatus}")

    categories_src = os.path.join("reports", "categories.json")
    categories_dst = os.path.join("reports", "allure-results", "categories.json")

    os.makedirs("reports/allure-results", exist_ok=True)

    shutil.copy(categories_src, categories_dst)

    generate_dashboard()

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
        help="Run headless"
    )

    parser.addoption(
        "--module",
        action="store",
        default="login"
    )