import json
import os


def load_json(path):
    """
    安全读取JSON
    """
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_dashboard():

    summary_path = "reports/execution_summary.json"
    flaky_path = "reports/flaky_report.json"
    history_path = "reports/history.json"

    summary = load_json(summary_path)
    flaky_data = load_json(flaky_path)
    history = load_json(history_path)

    if not summary:
        print("execution_summary.json not found")
        return

    # ======================
    # KPI
    # ======================

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    success_rate = summary.get("success_rate", 0)
    avg_duration = summary.get("average_duration", 0)

    flaky_tests = flaky_data.get("flaky_tests", 0)
    flaky_rate = flaky_data.get("flaky_rate", 0)

    run_count = len(history.get("runs", []))

    # ======================
    # Module success
    # ======================

    modules = json.dumps(
        list(summary.get("module_success_rate", {}).keys())
    )

    rates = json.dumps([
        float(v.replace("%", ""))
        for v in summary.get("module_success_rate", {}).values()
    ])

    # ======================
    # Slow tests
    # ======================

    slow_cases = json.dumps([
        c["case"]
        for c in summary.get("slowest_cases", [])
    ])

    slow_durations = json.dumps([
        c["duration"]
        for c in summary.get("slowest_cases", [])
    ])

    # ======================
    # History trend
    # ======================

    times = json.dumps([
        r["time"]
        for r in history.get("runs", [])
    ])

    success_rates = json.dumps([
        r["success_rate"]
        for r in history.get("runs", [])
    ])

    # ======================
    # HTML
    # ======================

    html = f"""
<!DOCTYPE html>
<html>

<head>

<title>Automation Testing Analytics Platform</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f5f5f5;
}}

h1{{
color:#333;
}}

.card{{
background:white;
padding:20px;
margin:10px;
border-radius:8px;
box-shadow:0px 2px 5px rgba(0,0,0,0.1);
display:inline-block;
width:200px;
text-align:center;
}}

.chart-container{{
width:700px;
margin-top:40px;
}}

table{{
width:100%;
border-collapse:collapse;
margin-top:20px;
}}

th,td{{
border:1px solid #ddd;
padding:8px;
}}

th{{
background:#4CAF50;
color:white;
}}

</style>

</head>


<body>

<h1>Automation Testing Analytics Platform</h1>

<div class="card">
<h2>Total Tests</h2>
<p>{total}</p>
</div>

<div class="card">
<h2>Passed</h2>
<p>{passed}</p>
</div>

<div class="card">
<h2>Failed</h2>
<p>{failed}</p>
</div>

<div class="card">
<h2>Success Rate</h2>
<p>{success_rate}%</p>
</div>

<div class="card">
<h2>Avg Duration</h2>
<p>{avg_duration}s</p>
</div>

<div class="card">
<h2>Flaky Tests</h2>
<p>{flaky_tests}</p>
</div>

<div class="card">
<h2>Flaky Rate</h2>
<p>{flaky_rate}%</p>
</div>

<div class="card">
<h2>Total Runs</h2>
<p>{run_count}</p>
</div>


<h2>Test Status Distribution</h2>

<div class="chart-container">
<canvas id="statusChart"></canvas>
</div>


<h2>Module Stability</h2>

<div class="chart-container">
<canvas id="moduleChart"></canvas>
</div>


<h2>Slowest Test Cases</h2>

<div class="chart-container">
<canvas id="slowChart"></canvas>
</div>


<h2>Success Rate Trend</h2>

<div class="chart-container">
<canvas id="trendChart"></canvas>
</div>


<h2>Slowest Test Cases Table</h2>

<table>

<tr>
<th>Module</th>
<th>Case</th>
<th>Duration</th>
</tr>
"""

    for case in summary.get("slowest_cases", []):

        html += f"""
<tr>
<td>{case["module"]}</td>
<td>{case["case"]}</td>
<td>{case["duration"]}s</td>
</tr>
"""

    html += "</table>"

    html += """
<h2>Module Success Rate</h2>

<table>

<tr>
<th>Module</th>
<th>Success Rate</th>
</tr>
"""

    for module, rate in summary.get("module_success_rate", {}).items():

        html += f"""
<tr>
<td>{module}</td>
<td>{rate}</td>
</tr>
"""

    html += "</table>"

    html += f"""

<script>

// pass / fail pie
new Chart(
document.getElementById('statusChart'),
{{
type:'pie',
data:{{
labels:['Passed','Failed'],
datasets:[{{
data:[{passed},{failed}],
backgroundColor:['#4CAF50','#F44336']
}}]
}}
}}
);


// module stability
new Chart(
document.getElementById('moduleChart'),
{{
type:'bar',
data:{{
labels:{modules},
datasets:[{{
label:'Success Rate',
data:{rates},
backgroundColor:'#2196F3'
}}]
}},
options:{{
scales:{{
y:{{
beginAtZero:true,
max:100
}}
}}
}}
}}
);


// slow tests
new Chart(
document.getElementById('slowChart'),
{{
type:'bar',
data:{{
labels:{slow_cases},
datasets:[{{
label:'Duration (s)',
data:{slow_durations},
backgroundColor:'#FF9800'
}}]
}}
}}
);


// success trend
new Chart(
document.getElementById('trendChart'),
{{
type:'line',
data:{{
labels:{times},
datasets:[{{
label:'Success Rate',
data:{success_rates},
borderColor:'#4CAF50',
fill:false
}}]
}}
}}
);

</script>

</body>

</html>
"""

    os.makedirs("reports", exist_ok=True)

    with open("reports/analytics_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Analytics dashboard generated: reports/analytics_dashboard.html")