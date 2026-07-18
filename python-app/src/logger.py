import os
import logging
import datetime
import pathlib

logger = logging.getLogger("python-app")
logger.setLevel(logging.INFO)


def get_logs_dir() -> str:
    """Return the path to the service's logs directory."""
    current_dir_name = pathlib.Path(__file__).parent
    module_main_path, _ = os.path.split(current_dir_name)
    logs_dir_name = "logs"
    return os.path.join(module_main_path, logs_dir_name)


def configure_logging(logs_dir: str) -> str:
    """Attach a file handler and a console handler to the logger, if not already configured.

    Returns the path to the log file being written; on repeat calls, the path
    already used by the existing file handler.
    """
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename

    os.makedirs(logs_dir, exist_ok=True)
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logs_file_path = os.path.join(logs_dir, f"{time_stamp}-python-app.log")

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s")

    file_handler = logging.FileHandler(logs_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logs_file_path
