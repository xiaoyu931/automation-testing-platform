import logging
import os
from datetime import datetime


def get_logger(name="automation"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    # 创建 logs 目录
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 按日期生成日志文件
    log_file = os.path.join(
        "logs",
        f"{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger