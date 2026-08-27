import logging

from config.settings import BrainConfig
from core.logging import setup_logging


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    config = BrainConfig()
    logger.info("%s starting", config.assistant_name)
    # Application startup logic here


if __name__ == "__main__":
    main()