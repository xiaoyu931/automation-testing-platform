import shutil
import os

# 删除旧结果
shutil.rmtree("reports/allure-results", ignore_errors=True)

# 运行测试
os.system("pytest --alluredir=reports/allure-results")

# 导出CSV
from utils.test_result_exporter_v1 import export_results
export_results()