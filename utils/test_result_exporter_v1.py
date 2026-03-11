import json
import os
import csv
import datetime


ALLURE_RESULTS = "reports/allure-results"
OUTPUT_FILE = "reports/test_results.csv"


def export_results():

    rows = []

    run_date = datetime.date.today()

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

        rows.append({
            "run_date": run_date,
            "test_name": name,
            "module": module,
            "status": status,
            "duration": duration
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=["run_date", "test_name", "module", "status", "duration"]
        )

        writer.writeheader()

        writer.writerows(rows)

    print("Test results exported:", OUTPUT_FILE)