@echo off

pytest -m "not failure" --alluredir=reports/allure-results --clean-alluredir
:: pytest -m flaky --alluredir=reports/allure-results --clean-alluredir
allure serve reports/allure-results