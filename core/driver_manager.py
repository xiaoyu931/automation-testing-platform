from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

class DriverManager:

    # 创建一个专门管理浏览器的类
    @staticmethod
    def create_driver(browser: str = "chrome", headless: bool = False):
        try:
            if browser == "chrome":
                # 创建浏览器参数对象
                options = ChromeOptions()
                # 若为False , 无头运行（没有界面） 常用于 CI/CD 服务器
                if headless:
                    options.add_argument("--headless=new")
                # 浏览器启动参数  启动时最大化
                options.add_argument("--start-maximized")
                # 禁止“Chrome 正受到自动化控制”提示
                options.add_argument("--disable-infobars")
                # 禁用插件，提高稳定性
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-notifications")
                options.add_argument("--disable-save-password-bubble")

                # 关闭 Chrome 密码管理器和密码泄露提示
                options.add_experimental_option(
                    "prefs",
                    {
                        "credentials_enable_service": False,
                        "profile.password_manager_enabled": False,
                        "profile.password_manager_leak_detection": False
                    }
                )

                # 创建浏览器实例  webdriver.Chrome 启动浏览器
                driver = webdriver.Chrome(
                    # ChromeDriverManager 自动下载驱动  Service 指定驱动路径
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            elif browser == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless=new")
                # 浏览器启动参数  启动时最大化
                options.add_argument("--start-maximized")
                # 禁止“Chrome 正受到自动化控制”提示
                options.add_argument("--disable-infobars")
                # 禁用插件，提高稳定性
                options.add_argument("--disable-extensions")
                driver = webdriver.Edge(
                    service=EdgeService("drivers/msedgedriver.exe"),
                    options=options
                )
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            # 等待机制
            driver.implicitly_wait(0)  # 禁止隐式等待   推荐用显式等待（WebDriverWait）  更可控，更稳定
             # 页面加载最多等 30 秒  超时会报错  防止页面卡死
            driver.set_page_load_timeout(30)
            # 把浏览器对象交给测试代码
            return driver
        except Exception as e:
            print("Driver 初始化失败:", e)
            raise

    @staticmethod
    # 关闭浏览器方法
    def quit_driver(driver):
        if driver:
            #安全关闭浏览器  防止 driver 为 None 报错
            driver.quit()
