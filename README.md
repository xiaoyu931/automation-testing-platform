# Automation Testing Platform

This project demonstrates a complete UI automation testing platform built with **Python + Pytest + CI/CD**.

It includes:

- Data-driven testing
- Retry mechanism
- Flaky test detection
- Allure reporting
- Test analytics dashboard
- CI pipeline with GitHub Actions
- Quality Gate for test reliability

---

# Features

✔ Pytest Automation Framework
✔ Page Object Model
✔ Data Driven Testing (YAML)
✔ Retry Mechanism
✔ Flaky Test Detection
✔ Allure Reporting
✔ Test Analytics (CSV + Dashboard)
✔ CI/CD with GitHub Actions
✔ Quality Gate (Success Rate Control)

---

# Project Structure
tests/ test cases
pages/ page objects
data/ test data
core/ framework core
hooks/ pytest hooks
utils/ utilities
reports/ generated reports


---

# CI Pipeline

Push code
↓
GitHub Actions
↓
Run Pytest
↓
Generate Allure Report
↓
Export Test Analytics
↓
Generate Dashboard
↓
Deploy to GitHub Pages

---

# Dashboard

The automation dashboard shows:

- Success rate trend
- Module stability
- Slowest test cases
- Flaky test detection

---

# Technology Stack

- Python
- Pytest
- Selenium
- Allure Report
- GitHub Actions
- Chart.js