import json
import os
import csv
from datetime import datetime

ALLURE_RESULTS = "reports/allure-results"
OUTPUT_FILE = "reports/test_execution.csv"


def get_failure_type(trace):

    if "AssertionError" in trace:
        return "Assertion Failure"

    if "TimeoutException" in trace:
        return "UI Timeout"

    if "NoSuchElementException" in trace:
        return "Locator Error"

    if "StaleElementReferenceException" in trace:
        return "Stale Element"

    return ""


def export_results():

    rows = []

    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for file in os.listdir(ALLURE_RESULTS):

        if not file.endswith("-result.json"):
            continue

        path = os.path.join(ALLURE_RESULTS, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        name = data.get("name")

        status = data.get("status")

        # 计算duration
        start = data.get("start")
        stop = data.get("stop")

        if start and stop:
            duration = round((stop - start) / 1000, 3)
        else:
            duration = 0

        labels = data.get("labels", [])

        module = "unknown"

        for l in labels:
            if l["name"] == "suite":
                module = l["value"]

        trace = ""
        # 判断 JSON 里有没有 statusDetails，如果有，就从里面取 trace， 一般是失败了才有
        if "statusDetails" in data:
            trace = data["statusDetails"].get("trace", "")

        failure_type = get_failure_type(trace)

        rows.append({
            "execution_time": execution_time,
            "test_name": name,
            "module": module,
            "status": status,
            "duration": duration,
            "failure_type": failure_type
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "execution_time",
                "test_name",
                "module",
                "status",
                "duration",
                "failure_type"
            ]
        )

        writer.writeheader()

        writer.writerows(rows)

    print("Export completed:", OUTPUT_FILE)