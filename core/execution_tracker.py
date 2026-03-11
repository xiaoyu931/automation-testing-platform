from collections import defaultdict

# retry 统计
retry_tracker = defaultdict(int)

# flaky test 记录
flaky_tests = []

class CurrentTest:
    value = None

current_test = CurrentTest()