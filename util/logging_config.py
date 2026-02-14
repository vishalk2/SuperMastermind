import os
import logging

from logging.handlers import RotatingFileHandler
from util.constants import (
    APP_NAME,
    LOG_DIRECTORY,
    LOG_FILENAME,
    LOG_FORMAT,
    LOG_DATETIME,
)


_LOGGER_INITIALIZED = False


def setup_logging() -> None:
    """
    Sets up application-wide logging configuration.
    Safe to call multiple times.
    """
    global _LOGGER_INITIALIZED

    if _LOGGER_INITIALIZED:
        return

    try:
        os.makedirs(LOG_DIRECTORY, exist_ok=True)
        log_filepath = os.path.join(LOG_DIRECTORY, LOG_FILENAME)

        if os.path.exists(log_filepath):
            with open(log_filepath, "w", encoding="utf-8"):
                pass

        logging_format = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=LOG_DATETIME,
        )

        root_logger = logging.getLogger(APP_NAME)
        root_logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler(
            log_filepath,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging_format)

        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        _LOGGER_INITIALIZED = True

    except Exception:
        print("CRITICAL: Failed to initialize logging system.")
        import traceback

        traceback.print_exc()
