import logging

from config.settings import BrainConfig
from core.logging import setup_logging


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    config = BrainConfig()
    logger.info("%s (%s) application starting", config.assistant_name, config.assistant_full_name)
    # Application startup logic here


if __name__ == "__main__":
    main()