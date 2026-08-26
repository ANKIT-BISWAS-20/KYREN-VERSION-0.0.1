import logging
import sys

from config.settings import LOG_DIR, LOG_FILE

LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> None:
    """Configure application-wide logging."""

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()

    root_logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if setup_logging() is called twice
    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)