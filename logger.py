import os
import logging
from datetime import datetime


def setup_logging() -> None:
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_directory, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_directory, f"scraper_{current_time}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
