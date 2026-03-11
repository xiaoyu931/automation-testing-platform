import os
import allure
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

class ScreenshotManager:

    @staticmethod
    def capture(driver, module_name, case_name, retry_index=None):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        retry_part = f"_retry{retry_index}" if retry_index else ""

        filename = f"{module_name}_{case_name}{retry_part}_{timestamp}.png"
        screenshot_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        file_path = os.path.join(screenshot_dir, filename)

        driver.save_screenshot(file_path)

        # attach to allure
        # 把一个文件添加到 Allure 测试报告中
        allure.attach.file(
            file_path,
            name=filename,
            # 告诉 Allure 这个文件是什么类型,这里是PNG,说明它是图片格式,常见类型还有allure.attachment_type.JSON
            attachment_type=allure.attachment_type.PNG
        )

        logger.error(f"Screenshot saved: {file_path}")

        return file_path

