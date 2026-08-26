import logging

from core.logging import setup_logging


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Jarvis application starting")
    # Application startup logic here


if __name__ == "__main__":
    main()