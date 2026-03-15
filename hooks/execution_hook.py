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
#case_execution_data用于记录每一次测试执行结果，是每一次测试，不是每一个测试
case_execution_data = []

# 测试开始时执行
def pytest_sessionstart(session):
    # 记录 测试开始时间
    execution_data["start_time"] = time.time()

    # 清空上次运行数据
    retry_tracker.clear()
    flaky_tests.clear()
    case_execution_data.clear()

# 所有测试执行完成后运行
def pytest_sessionfinish(session, exitstatus):

    execution_data["end_time"] = time.time()
    # total execution time
    duration = execution_data["end_time"] - execution_data["start_time"]
    # 读取运行参数 来自命令：pytest --env stage --browser chrome
    env = session.config.getoption("--env")
    browser = session.config.getoption("--browser")
    # 获取默认配置
    settings = Settings(env)
    browser = browser or settings.default_browser
    threshold = settings.get_success_threshold

    avg_duration = 0
    slowest_cases = []
    module_success_rate = {}
    top_failed_cases = []

    if case_execution_data:
        # 计算平均执行时间
        avg_duration = sum(
            case["duration"] for case in case_execution_data
        ) / len(case_execution_data)
        # 找到执行最慢的5个测试  按照每个元素的 duration 值进行排序
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
        # 创建一个字典，如果访问不存在的 module，就自动创建：{"total": 0, "passed": 0}
        module_stats = defaultdict(lambda: {"total": 0, "passed": 0})

        for case in case_execution_data:
            module = case["module"]
            # 这个模块执行的测试用例数量 +1
            module_stats[module]["total"] += 1
            # 如果成功就统计 passed
            if case["status"] == "passed":
                module_stats[module]["passed"] += 1

        for module, stats in module_stats.items():

            rate = round(
                stats["passed"] / stats["total"] * 100,
                2
            )

            module_success_rate[module] = f"{rate}%"
        # 哪个case失败最多  创建一个字典，用来 统计每个测试用例失败次数。默认值是0
        fail_counter = defaultdict(int)

        for case in case_execution_data:

            if case["status"] == "failed":
                key = f"{case['module']}::{case['case']}"
                fail_counter[key] += 1
        # x[1] = count
        top_failed_cases = [
            {"case": case, "count": count}
            for case, count in sorted(
                fail_counter.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]

    # -------- 计算最终成功率（忽略 retry 中间失败） --------

    final_results = {}

    for case in case_execution_data:
        # 如果 同一个 case 执行多次，字典会 只保留最后一次结果
        final_results[case["case"]] = case["status"]

    passed = sum(1 for v in final_results.values() if v == "passed")
    # 等价于：
    # passed = 0
    # for v in final_results.values():
    #     if v == "passed":
    #         passed += 1
    total = len(final_results)
    # 如果 total != 0，成功率 = passed / total * 100，否则为0
    success_rate = round(passed / total * 100, 2) if total else 0

    summary = {
        "env": env,
        "browser": browser,
        "total": execution_data["total"],
        "passed": execution_data["passed"],
        "failed": execution_data["failed"],
        "skipped": execution_data["skipped"],
        "total_duration": round(duration, 2),
        "success_rate": success_rate,
        "average_duration": round(avg_duration, 2),
        "slowest_cases": slowest_cases,
        "module_success_rate": module_success_rate,
        "top_failed_cases": top_failed_cases
    }

    os.makedirs("reports", exist_ok=True)

    with open("reports/execution_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # -------- 写入历史记录 --------

    history_file = "reports/history.json"
    # 如果文件不存在：返回{"runs": []}
    history_data = {"runs": []}
    # 读取之前的测试执行历史
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history_data = json.load(f)

    # -------- Flaky Test 检测 --------
    # Flaky Test 的意思，同一个测试有时成功，有时失败，最终是成功了
    # 假设数据：
    # case_execution_data
    # login_test failed
    # login_test passed
    # order_test passed
    #  生成：
    # case_runs = {
    #     "login_test": ["failed", "passed"],
    #     "order_test": ["passed"]
    # }
    # 创建一个字典，如果 key 不存在，就自动创建一个 空 list。相当于：
    # {
    #     key1: [],
    #     key2: [],
    #     key3: []
    # }
    # 但这些 key只有在使用时才创建。
    case_runs = defaultdict(list)

    for case in case_execution_data:
        case_runs[case["case"]].append(case["status"])
    # 检测 retry 成功的 case
    # case = login_test
    # runs = ["failed", "passed"]
    for case, runs in case_runs.items():

        retry_count = len(runs) - 1
        # 取最后一次执行结果
        final_status = runs[-1]
        # 判断flaky
        if retry_count > 0 and final_status == "passed":
            flaky_tests.append({
                "case": case,
                "retry": retry_count,
                "type": "retry_pass"
            })
    # 计算Flaky Rate
    # 去重
    unique_cases = set(c["case"] for c in case_execution_data)
    total_tests = len(unique_cases)
    flaky_count = len(flaky_tests)
    print("retry_tracker:", retry_tracker)
    print("case_execution_data:", case_execution_data)

    flaky_rate = 0

    if total_tests > 0:
        flaky_rate = round(flaky_count / total_tests * 100, 2)

    # -------- history 记录 --------

    run_record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": summary["total"],
        "passed": summary["passed"],
        "failed": summary["failed"],
        "success_rate": summary["success_rate"],
        "avg_duration": summary["average_duration"],
        "flaky_rate": flaky_rate
    }
    # 记录一次自动化测试运行结果
    history_data["runs"].append(run_record)
    # 并只保存最近50次执行历史
    history_data["runs"] = history_data["runs"][-50:]
    #  生成reports/history.json，用于测试趋势分析
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)

    # -------- Flaky 报告 --------

    with open("reports/flaky_tests.json", "w", encoding="utf-8") as f:
        json.dump({"flaky_tests": flaky_tests}, f, indent=4)

    flaky_report = {
        "total_tests": total_tests,
        "flaky_tests": flaky_count,
        "flaky_rate": flaky_rate,
        "unstable_tests": flaky_tests
    }

    with open("reports/flaky_report.json", "w", encoding="utf-8") as f:
        json.dump(flaky_report, f, indent=4)

    # -------- Quality Gate --------

    if summary["success_rate"] < threshold:

        print(f"\n⚠ Success rate below {threshold}%! Failing build.")
        # CI 会认为：BUILD FAILED
        session.exitstatus = 1

    print(f"\nFinal exit status: {session.exitstatus}")

    # -------- Allure categories --------
    # Allure 报告配置
    categories_src = os.path.join("reports", "categories.json")
    categories_dst = os.path.join("reports", "allure-results", "categories.json")

    os.makedirs("reports/allure-results", exist_ok=True)

    if os.path.exists(categories_src):
        # 把：reports/categories.json复制到：allure-results，用于：Allure错误分类
        shutil.copy(categories_src, categories_dst)

    # -------- 生成 Dashboard --------

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