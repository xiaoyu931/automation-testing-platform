class ConfigLoader:
    def load(self):
        print("加载配置")
        return {"case" : "demo"}

class Logger:
    def __init__(self, fileName="log.txt"):
        self.fileName = fileName

    def log(self, message):
        with open(self.fileName, "a", encoding="utf-8") as f:
            f.write(message + "\n")
        print(f"[LOG] {message}")

class TestExecutor:
    def execute(self, case):
        print(f"执行测试：{case}")
        return  True

class TestRunner:
    def __init__(self):
        self.config = ConfigLoader()
        self.logger = Logger()
        self.executor = TestExecutor()

    def run(self):
        data = self.config.load()
        result = self.executor.execute(data["case"])
        self.logger.log(f"执行结果：{result}")
        return result


if __name__ == '__main__':
    testRunner_1 = TestRunner()
    testRunner_1.run()



