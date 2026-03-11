import json
import os
import csv
from datetime import datetime

ALLURE_RESULTS = "reports/allure-results"
HISTORY_FILE = "reports/test_history.csv"


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


def get_next_run_id():

    if not os.path.exists(HISTORY_FILE):
        return 1

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return 1

    last = max(int(r["run_id"]) for r in rows)

    return last + 1


def export_history():

    run_id = get_next_run_id()

    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []

    for file in os.listdir(ALLURE_RESULTS):

        if not file.endswith("-result.json"):
            continue

        path = os.path.join(ALLURE_RESULTS, file)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        name = data.get("name")

        status = data.get("status")

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

        if "statusDetails" in data:
            trace = data["statusDetails"].get("trace", "")

        failure_type = get_failure_type(trace)

        rows.append({
            "run_id": run_id,
            "execution_time": execution_time,
            "test_name": name,
            "module": module,
            "status": status,
            "duration": duration,
            "failure_type": failure_type
        })

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_id",
                "execution_time",
                "test_name",
                "module",
                "status",
                "duration",
                "failure_type"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)

    print("History exported run_id:", run_id)