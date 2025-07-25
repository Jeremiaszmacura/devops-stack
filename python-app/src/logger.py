import os
import logging
import datetime
import pathlib


def create_logger(logs_dir: str) -> tuple:
    os.makedirs(logs_dir, exist_ok=True)
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logs_filename = f"{time_stamp}-python-app.log"
    logs_file_path = os.path.join(logs_dir, logs_filename)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(logs_file_path)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger, logs_file_path


def get_logs_dir() -> str:
    current_dir_name = pathlib.Path(__file__).parent
    module_src_path, _ = os.path.split(current_dir_name)
    module_main_path, _ = os.path.split(module_src_path)
    logs_dir_name = "logs"
    logs_dir = os.path.join(module_main_path, logs_dir_name)
    return logs_dir


logs_dir = get_logs_dir()
logger, logs_file_path = create_logger(logs_dir)
logger.info(f"Logger configured. Logs path: {logs_file_path}")